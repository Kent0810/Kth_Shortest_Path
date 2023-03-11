import json
import random
import time

import pygame

pygame.font.init()
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color('white')
FONT = pygame.font.SysFont('Arial', 20)

ENDPOINT_WIDTH = 25
CAR_RADIUS = 5
ARRIVE_THRESHOLD = 5

WINDOW_WIDTH = 750
WINDOW_HEIGHT = 750

TIME_TO_DEST = 1
FPS = 60
FPS_TO_DEST = FPS * TIME_TO_DEST


class Counter:
    """Count and calculate counting speed."""
    def __init__(self):
        self.start_time = 0
        self.counted = 0

    def increase(self):
        self.counted += 1
        # Start the timer as soon as `counted` is increased
        if self.start_time == 0:
            self.start_time = time.time()

    def get_rate(self):
        if self.start_time > 0:
            return self.counted / max(time.time() - self.start_time, 1)
        else:
            return 0.0


class Endpoint:
    """Endpoint object with convenient blit method."""
    def __init__(self, endpoint_index, position: pygame.Vector2, width, color):
        self.index = endpoint_index
        self.position = position
        self.width = width
        self.color = color
        self.outgoing = Counter()
        self.arriving = Counter()

        self.index_text = FONT.render(str(self.index), True, BLACK)
        self.index_text.blit(FONT.render(str(self.index), True, WHITE),
                             [-1, -1, 0, 0])

    def blit(self, surface: pygame.Surface):
        """Blit this endpoint to a surface at self.position."""
        # Draw endpoint circle
        pygame.draw.circle(surface, BLACK, self.position, self.width + 1)
        pygame.draw.circle(surface, self.color, self.position, self.width)
        blit_at_center(surface, self.index_text, self.position)

        self.blit_cars_rates(surface)

    def blit_cars_rates(self, surface):
        """Blit cars outgoing and arriving rates (speed)"""
        outgoing_text = FONT.render(
            f"{round(self.outgoing.get_rate(), 1)} cars/s",
            True,
            pygame.Color('green')
        )
        arriving_text = FONT.render(
            f"{round(self.arriving.get_rate(), 1)} cars/s",
            True,
            pygame.Color('red')
        )

        # Calculate blit rects and display them
        font_height = FONT.get_height()
        outgoing_text_offset = pygame.Vector2(0, self.width + font_height / 2)
        arriving_text_offset = pygame.Vector2(0, self.width + font_height * 1.5)
        outgoing_text_pos = self.position + outgoing_text_offset
        arriving_text_pos = self.position + arriving_text_offset
        pygame.draw.rect(surface,
                         BLACK,
                         outgoing_text.get_rect(center=outgoing_text_pos.xy))
        pygame.draw.rect(surface,
                         BLACK,
                         arriving_text.get_rect(center=arriving_text_pos.xy))
        blit_at_center(surface, outgoing_text, outgoing_text_pos)
        blit_at_center(surface, arriving_text, arriving_text_pos)


class Car:
    """Car object with auto moving and endpoints interacting."""
    def __init__(self, source: Endpoint, dest: Endpoint):
        self.source = source
        self.dest = dest

        # Init car position with some random offset from source.position
        self.position = source.position + random_pos_vector()
        # Use velocity vector to simplify moving calculations
        self.velocity = (dest.position - source.position) / (TIME_TO_DEST * FPS)

        self.color = source.color
        self.started = False
        self.arrived = False

    def blit(self, surface: pygame.Surface):
        """Blit car onto surface and move the car a distance."""
        if not self.arrived:
            self.position += self.velocity
            pygame.draw.circle(surface, self.color, self.position, CAR_RADIUS)

            # Detect car arriving
            distance_to_dest = self.position.distance_to(self.dest.position)
            if distance_to_dest < self.dest.width - ARRIVE_THRESHOLD:
                self.arrived = True
                self.dest.arriving.increase()

            # Increase source.outgoing counter
            if not self.started:
                self.source.outgoing.increase()
                self.started = True


def visualize(flow_graph, endpoints_map,
              num_cars=1e3):
    """Visualize max flow graph with cars moving from endpoints to endpoints."""
    pygame.init()
    screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
    clock = pygame.time.Clock()

    endpoints = create_endpoints(len(flow_graph), endpoints_map, ENDPOINT_WIDTH,
                                 WINDOW_WIDTH, WINDOW_HEIGHT)
    cars = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Add more cars to meet `num_cars` limit with controlled adding speed
        added = 0
        while len(cars) < num_cars and added * FPS_TO_DEST < num_cars:
            cars.append(create_random_car(flow_graph, endpoints))
            added += 1

        # Display cars and endpoints
        screen.fill(BLACK)

        for car in cars:
            car.blit(screen)
            if car.arrived:
                cars.remove(car)
        for endpoint in endpoints:
            endpoint.blit(screen)

        pygame.display.update()
        clock.tick(60)
        fps = round(clock.get_fps(), 1)
        pygame.display.set_caption(f"Max flow - FPS {fps}")


def get_random_colors(num_colors):
    """Generate random colors with evenly spaced hue values."""
    colors = []
    hue_spacing = 360 // num_colors
    hue_start = random.randrange(0, hue_spacing)

    for hue in range(hue_start, 360, hue_spacing):
        # Generate color with random saturation and lightness
        saturation = random.randint(60, 80)
        lightness = random.randint(40, 60)
        color = pygame.Color(0, 0, 0)
        color.hsla = [hue, saturation, lightness, 100]
        colors.append(color)

    return colors


def random_pos_vector():
    """Get random offset vector, used for Car positioning."""
    random_range = ENDPOINT_WIDTH - ARRIVE_THRESHOLD
    vector = pygame.Vector2(random.random() * random_range, 0)
    vector.rotate_ip(random.randint(0, 360))
    return vector


def create_endpoints(endpoints_count, endpoints_map, endpoint_width,
                     window_width, window_height):
    """Create endpoints with positions from endpoints_map."""
    grid_spacing = min(
        window_height / (len(endpoints_map) + 1),
        window_width / (len(endpoints_map[0]) + 1)
    )
    display_rect = pygame.Rect(0, 0,
                               grid_spacing * (len(endpoints_map[0]) - 1),
                               grid_spacing * (len(endpoints_map)) - 1)
    display_rect.center = window_width / 2, window_height / 2
    endpoints = []
    colors = get_random_colors(endpoints_count)
    for ind in range(endpoints_count):
        endpoint = Endpoint(ind,
                            pygame.Vector2(display_rect.topleft),
                            endpoint_width,
                            colors[ind])
        endpoints.append(endpoint)
    for row_ind, row in enumerate(endpoints_map):
        for col_ind, number in enumerate(row):
            if number >= 0:
                endpoints[number].position += pygame.Vector2(
                    col_ind * grid_spacing,
                    row_ind * grid_spacing
                )
    return endpoints


def create_random_car(flow_graph, endpoints):
    row_weights = [sum(row) for row in flow_graph]
    row_indexes = range(len(row_weights))
    row_ind = random.choices(row_indexes,
                             weights=row_weights,
                             k=1)[0]
    col_ind = random.choices(range(len(flow_graph[row_ind])),
                             weights=flow_graph[row_ind],
                             k=1)[0]
    return Car(endpoints[row_ind], endpoints[col_ind])


def blit_at_center(dest_surface: pygame.Surface, source_surface: pygame.Surface,
                   center: pygame.Vector2):
    dest_surface.blit(source_surface,
                      source_surface.get_rect(center=center.xy))


if __name__ == '__main__':
    map_lines = open('map.txt').read().splitlines()
    ends_map = [
        [int(i) for i in line.split()] for line in map_lines
    ]
    visualize(json.load(open('flow_graph.json')), ends_map)

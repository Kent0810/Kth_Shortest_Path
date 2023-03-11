#include<iostream>
using namespace std;

int cost[100][100], n, k;

int results[100];


int dijkstra(int src, int end, int k);
void display(int dist[], int par[], int end, int src) {
    fill(results, results + n, INT_MAX);
    int temp = end;
    int i = 0;
    while (temp != -1) {
        results[i] = temp;
        temp = par[temp];
        i++;
    }
    int flag = 0, size = 0;
    while (results[size] != INT_MAX) size++;
    while (results[flag] != INT_MAX) {
        if (flag < size - 1) {
            cout << results[flag] << "<-";
        }
        else {
            cout << results[flag];
        }
        flag++;
    }
    //this just to output the entire matrix
    cout << endl;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cout << cost[i][j] << " ";
        }
        cout << endl;
    }
    cout << endl;
    cout << "Distance To The End Node Is" << endl;
    cout << "::::Distance = " << dist[end];
    cout << endl;
}
int key = 0;
int tempCost[100][100];

void changeCostMatrix() {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cost[i][j] = tempCost[i][j];
        }
    }
}
void sealUp() {
    for (int i = 0; i < 100; i++) {
        for (int j = 0; j < 100; j++) {
            tempCost[i][j] = cost[i][j];
        }
    }
}
void removeEdge(int src, int end) {
    cost[src][end] = 999;
}
int pickShorter(int candidatePath[]) {
    int flag = 0;
    int min = candidatePath[0];
    int result = 0;
    while (candidatePath[flag] != INT_MAX) {
        if (candidatePath[flag] < min) {
            min = candidatePath[flag];
            result = flag;
        }
        flag++;
    }
    return result;
}



void kshortest(int src, int end, int k) {
    int candidatePath[100], shortestPath[100];
    if (k > 0) {
        shortestPath[0] = dijkstra(src, end, k);
    }
    //iterate through the whole results matrix and remove k-1 edge from the shortest path
    if (k > 1) {
        for (int z = 0; z < k - 1; z++) {
            fill(shortestPath + 1, shortestPath + n, INT_MAX);
            int  resultSize = 0;
            int flag = 0;
            while (results[flag] != INT_MAX) {
                flag++;
                resultSize++;
            }
            fill(candidatePath, candidatePath + resultSize, INT_MAX);
            for (int i = 0; i < resultSize; i++) {
                shortestPath[i] = results[i];
            }
            for (int i = 0; i < resultSize - 1; i++) {
                cout << endl << i + 1 << " ITERATION!";
                removeEdge(shortestPath[i + 1], shortestPath[i]);
                candidatePath[i] = dijkstra(src, end, k);
                changeCostMatrix();//restore it back to normal for next iteration
            }
            int final_result = pickShorter(candidatePath);
            cout << endl << k << " th Shortest Path Is: ";
            removeEdge(shortestPath[final_result + 1], shortestPath[final_result]);
            sealUp();
            //made the cost matrix never revive
            dijkstra(src, end, k);
        }
    }
}

int getMin(int dist[], bool visited[]) {
    int key = 0;
    int min = INT_MAX;
    for (int i = 0; i < n; i++) {
        if (!visited[i] && dist[i] < min) {
            min = dist[i];
            key = i;
        }
    }
    return key;
}

int dijkstra(int src, int end, int k) {
    int par[100], dist[100];
    bool visited[100] = { 0 };
    //fill from dist -> dist +n with INT_MAX
    fill(dist, dist + n, INT_MAX);
    dist[src] = 0;
    par[src] = -1;
    //iterate through all node except the final node
    for (int g = 0; g < n - 1; g++) {
        //get NearestUnvistedNode 
        int u = getMin(dist, visited);
        visited[u] = true;
        //cout << " min = " << u << endl;
        for (int v = 0; v < n; v++) {
            if (!visited[v] && (dist[u] + cost[u][v]) < dist[v] && cost[u][v] != 999)
            {
                par[v] = u;
                dist[v] = dist[u] + cost[u][v];
            }
        }
    }
    cout << endl;
    display(dist, par, end, src);
    return dist[end];
}

int main() {
    cout << "Enter verticies : ";
    cin >> n;
    cout << "Enter adjacency matrix : \n";

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cin >> cost[i][j];
        }
    }
    for (int i = 0; i < 100; i++) {
        for (int j = 0; j < 100; j++) {
            tempCost[i][j] = cost[i][j];
        }
    }
    int src, end, k;
    cout << "\nEnter source : "; {
        cin >> src;
    }
    cout << "\nEnter destination : "; {
        cin >> end;
    }
    cout << "\nEnter Kth : "; {
        cin >> k;
    }
    kshortest(src, end, k);
}





//input test 
/*999 10 15 999 999 999
999 999 999 12 999 15
999 999 999 999 10 999
999 999 999 999 2 1
999 999 999 999 999 999
999 15 999 1 5 999*/


//input test final
/*
999 999 999 999 1 999
999 999 1 999 999 999
999 999 999 999 999 1
1 999 999 999 1 999
999 1 999 999 999 1
999 999 999 999 999 999
*/
/*
999 4 999 999 999 999 999 8 999
4 999 8 999 999 999 999 11 999
999 8 999 7 999 4 999 999 8
999 999 7 999 9 14 999 999 999
999 999 999 9 999 10 999 999 999
999 999 4 14 10 999 2 999 999
999 999 999 999 999 2 999 1 6
8 11 999 999 999 999 1 999 7
999 999 2 999 999 6 999 7 999
*/
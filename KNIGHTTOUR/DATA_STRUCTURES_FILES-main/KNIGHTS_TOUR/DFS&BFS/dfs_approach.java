// Depth First

import java.util.Scanner;

public class dfs_approach {
    static int N = 8;
    static int[][] chessBoard = new int[N][N];
    static int[] xMoves = {2, 1, -1, -2, -2, -1, 1, 2};
    static int[] yMoves = {1, 2, 2, 1, -1, -2, -2, -1};

    static boolean isSafe(int x, int y) {
        return (x >= 0 && x < N && y >= 0 && y < N && chessBoard[x][y] == -1);
    }

    static boolean findTour(int x, int y, int moveNumber) {
        if (moveNumber == N * N) {
            return true;
        }

        for (int i = 0; i < N; i++) {
            int newX = x + xMoves[i];
            int newY = y + yMoves[i];
            if (isSafe(newX, newY)) {
                chessBoard[newX][newY] = moveNumber;
                if (findTour(newX, newY, moveNumber + 1)) {
                    return true;
                } else {
                    chessBoard[newX][newY] = -1;
                }
            }
        }

        return false;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the starting coordinates of the knight:");
        int x = sc.nextInt();
        int y = sc.nextInt();
        sc.close();

        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                chessBoard[i][j] = -1;
            }
        }

        chessBoard[x][y] = 0;

        if (findTour(x, y, 1)) {
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < N; j++) {
                    System.out.print(chessBoard[i][j] + " ");
                }
                System.out.println();
            }
        } else {
            System.out.println("No solution found.");
        }
    }
}



//Breadth First Approach

import java.util.ArrayDeque;
import java.util.Queue;
import java.util.Scanner;

public class bfs_approach {
    private static final int[] ROW_MOVES = {2, 1, -1, -2, -2, -1, 1, 2};
    private static final int[] COL_MOVES = {1, 2, 2, 1, -1, -2, -2, -1};

    private static boolean isValidMove(int[][] chessBoard, int row, int col, int numRows, int numCols) {
        return row >= 0 && row < numRows && col >= 0 && col < numCols && chessBoard[row][col] == -1;
    }

    public static boolean knightsTour(int[][] chessBoard, int numRows, int numCols, int startRow, int startCol, int moveNumber){
        Queue<Integer> rowQueue = new ArrayDeque<>();
        Queue<Integer> colQueue = new ArrayDeque<>();

        rowQueue.add(startRow);
        colQueue.add(startCol);

        chessBoard[startRow][startCol] = moveNumber;

        while (!rowQueue.isEmpty()) {
            int row = rowQueue.poll();
            int col = colQueue.poll();

            if (moveNumber == numRows * numCols - 1) {
                // we have completed a tour
                return true;
            }

            for (int i = 0; i < ROW_MOVES.length; i++) {
                int newRow = row + ROW_MOVES[i];
                int newCol = col + COL_MOVES[i];
                if (isValidMove(chessBoard, newRow, newCol, numRows, numCols)) {
                    chessBoard[newRow][newCol] = ++moveNumber;
                    rowQueue.add(newRow);
                    colQueue.add(newCol);
                }
            }
        }

        return false;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the starting coordinates of the knight:");
        int numRows = sc.nextInt();
        int numCols = sc.nextInt();
        int[][] chessBoard = new int[numRows][numCols];

        for (int i = 0; i < numRows; i++) {
            for (int j = 0; j < numCols; j++) {
                chessBoard[i][j] = -1;
            }
        }

        int startRow = 0;
        int startCol = 0;

        boolean tourCompleted = knightsTour(chessBoard, numRows, numCols, startRow, startCol, 0);

        if (tourCompleted) {
            System.out.println("Tour completed!");
            for (int i = 0; i < numRows; i++) {
                for (int j = 0; j < numCols; j++) {
                    System.out.print(chessBoard[i][j] + " ");
                }
                System.out.println();
            }
        } else {
            System.out.println("Tour not completed.");
        }
    }
}



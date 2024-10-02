import java.util.*;

class CycleSortApp {
    public static void sortCycle(int array[], int length) {
        int writeOps = 0;

        for (int start = 0; start <= length - 2; start++) {
            int currentItem = array[start];
            int position = start;

            for (int i = start + 1; i < length; i++) {
                if (array[i] < currentItem) {
                    position++;
                }
            }

            if (position == start) {
                continue;
            }

            while (currentItem == array[position]) {
                position += 1;
            }

            if (position != start) {
                int temp = currentItem;
                currentItem = array[position];
                array[position] = temp;
                writeOps++;
            }

            while (position != start) {
                position = start;

                for (int i = start + 1; i < length; i++) {
                    if (array[i] < currentItem) {
                        position++;
                    }
                }

                while (currentItem == array[position]) {
                    position += 1;
                }

                if (currentItem != array[position]) {
                    int temp = currentItem;
                    currentItem = array[position];
                    array[position] = temp;
                    writeOps++;
                }
            }
        }
    }

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        System.out.println("Enter the number of elements:");
        int size = input.nextInt();
        int[] userArray = new int[size];

        System.out.println("Enter the elements:");
        for (int i = 0; i < size; i++) {
            userArray[i] = input.nextInt();
        }

        sortCycle(userArray, size);

        System.out.println("Sorted array:");
        for (int i = 0; i < size; i++) {
            System.out.print(userArray[i] + " ");
        }
    }
}

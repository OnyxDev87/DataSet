import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        String filePath = "01 renewable-share-energy.csv";
        ArrayList<String> data = ReadFromFile.readFile(filePath);

        for (int i = 0; i < data.size(); i++) {
            String line = data.get(i);
            String[] values = line.split(",");
            for (int j = 0; j < values.length; j++) {
                System.out.print(values[j] + " ");
            }
            System.out.println();
        }
    }
}

class ReadFromFile {
    public static ArrayList<String> readFile(String filePath) {
        ArrayList<String> data = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = br.readLine()) != null) {
                data.add(line);
            }
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
        }

        return data;
    }
}

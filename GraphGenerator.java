import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.ui.ApplicationFrame;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class GraphGenerator extends ApplicationFrame {

    public GraphGenerator(String title) {
        super(title);

        XYSeries series = new XYSeries("Renewables (%)");

        String filePath = "01 renewable-share-energy.csv";
        String targetEntity = "World";

        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line = br.readLine(); // Skip header

            while ((line = br.readLine()) != null) {
                String[] values = line.split(",");

                if (values.length < 4) continue;

                String entity = values[0].trim();
                int year = Integer.parseInt(values[2].trim());
                double renewables = Double.parseDouble(values[3].trim());

                if (entity.equalsIgnoreCase(targetEntity)) {
                    series.add(year, renewables);
                }
            }
        } catch (IOException | NumberFormatException e) {
            System.err.println("Error: " + e.getMessage());
            return;
        }

        XYSeriesCollection dataset = new XYSeriesCollection(series);
        JFreeChart chart = ChartFactory.createXYLineChart(
                "Renewable Energy Share Over Time - " + targetEntity,
                "Year",
                "Renewables (%)",
                dataset
        );

        ChartPanel panel = new ChartPanel(chart);
        setContentPane(panel);
    }

    public static void main(String[] args) {
        GraphGenerator chart = new GraphGenerator("Renewable Energy Share");
        chart.setSize(800, 600);
        chart.setLocationRelativeTo(null);
        chart.setVisible(true);
    }
}

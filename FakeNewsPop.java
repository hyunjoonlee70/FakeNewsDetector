import javafx.application.Application;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Pane;
import javafx.stage.Stage;
import java.io.*;

public class FakeNewsPop extends Application {
	@Override
	public void start(Stage stage) {
		stage.setTitle("Fake News Detected!");
		PaneOrganizer organizer = new PaneOrganizer();
		Scene scene = new Scene(organizer.getRoot());
		stage.setResizable(false);
		stage.setScene(scene);
		stage.show();
		stage.centerOnScreen();
	}

	public static void main(String[] argv) {
		launch(argv);
	}
}

class PaneOrganizer {
	private BorderPane root;
	private Pane popup;
	private ImageView background;
	private HBox hb;

	public PaneOrganizer() {
		root = new BorderPane();


		hb = new HBox();
		hb.setAlignment(Pos.CENTER);
		hb.setSpacing(15);

		popup = new Pane();

		root.setCenter(popup);
		root.setBottom(hb);

		try {
			this.createPopUp();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private void createPopUp() throws IOException {
		FileWriter out = new FileWriter("answer.txt");

		popup.setFocusTraversable(true);
		popup.setPrefSize(300, 220);
		popup.setStyle("-fx-background-color: White;");
		Image Zuckerburg = new Image(getClass().getResourceAsStream("Fake news.png"), 426.72 / 2.0, 331.92 / 2.0, false,
				false);
		background = new ImageView();
		background.setImage(Zuckerburg);
		background.setSmooth(true);
		background.relocate(45, 20);
		popup.getChildren().addAll(background);

		Button yes = new Button("Yes");
		yes.addEventHandler(MouseEvent.MOUSE_CLICKED, event -> {
			try {
				out.write("yes");
				out.close();
			} catch (Exception e) {
				e.printStackTrace();
			}
			System.exit(0);
		});

		Button no = new Button("No");
		no.addEventHandler(MouseEvent.MOUSE_CLICKED, event -> {
			try {
				out.write("no");
				out.close();
			} catch (Exception e) {
				e.printStackTrace();
			}
			System.exit(0);
		});

		hb.getChildren().addAll(yes, no);


	}

	public Pane getRoot() {
		return root;
	}

}

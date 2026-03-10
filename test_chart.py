import sys
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Customer:
    def __init__(self, name, rating):
        self.Name = name
        self.Rating = rating

class TestStarChart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Feedback Star Chart")
        self.resize(800, 600)

        class Object: pass
        self.cus = Object()
        self.cus.list = [
            Customer("Khang", 5), Customer("An", 4), Customer("Bình", 5),
            Customer("Chi", 3), Customer("Dũng", 5), Customer("Hoa", 2),
            Customer("Tuấn", 4), Customer("Lan", 5), Customer("Minh", 1),
            Customer("Hải", 5), Customer("Yến", 4), Customer("Nam", 3)
        ]

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.show_feedback_chart()

    def show_feedback_chart(self):

        plt.rcParams['font.family'] = 'Segoe UI Emoji'

        star_counts = [0, 0, 0, 0, 0]
        for c in self.cus.list:
            try:
                star = int(c.Rating)
                if 1 <= star <= 5:
                    star_counts[star - 1] += 1
            except:
                pass

        stars = ["1⭐", "2⭐", "3⭐", "4⭐", "5⭐"]

        self.figure.clear()
        ax = self.figure.add_subplot(111)


        bars = ax.bar(stars, star_counts, color="#FFD700", edgecolor="#B8860B")


        ax.set_xticklabels(stars)
        tick_labels = ax.get_xticklabels()
        for label in tick_labels:
            label.set_color("black")    #cho nay de chinh mau cua ngoi sao
            label.set_fontweight('bold')
            label.set_fontsize(12)


        ax.set_title("Customer Feedback Rating Statistics", fontsize=14, fontweight='bold', color='black')
        ax.set_xlabel("Rating Level (Stars)", color="black", fontweight='bold')
        ax.set_ylabel("Number of Feedbacks", color="black")

        ax.set_ylim(0, max(star_counts) + 1)


        for i, v in enumerate(star_counts):
            ax.text(i, v + 0.1, str(v), ha='center', fontweight='bold', color='black')

        plt.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestStarChart()
    window.show()
    sys.exit(app.exec())
class ColoredWidget():
    """Special methods for styling QWidget objects
    """


    def setBackground(self, color: str = None):
        """Changes background color

        Args:
            color (str): Background property
        """
        self.setProperty("background", color)
        self._updateStyle()
        

    def setColor(self, color: str = None):
        """Changes text color

        Args:
            color (str): Color property
        """
        self.setProperty("color", color)
        self._updateStyle()
    

    def _updateStyle(self):
        """Forces this widget to update its CSS styles
        """
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
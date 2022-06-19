from tkinter import *
from tkinter import colorchooser
import numpy as np
import random
from tkinter.messagebox import *


def drawCircle(canvas, x0, y0, overlap):
    canvas.create_oval(10 + (overlap * x0), 10 + (overlap * y0), 100 + (overlap * x0), 100 + (overlap * y0), width=0,
                       fill="white")


class Player:
    def __init__(self):
        self.name = ""
        self.color = ""
        self.number = 0


class WindowInfoPlayers:
    def __init__(self, master):
        self.master = master
        self.master.title("Joueurs")
        self.master.geometry("720x300")
        self.player1 = Player()
        self.player1.color = "red"
        self.player1.name = "Joueur 1"
        self.player2 = Player()
        self.player2.color = "yellow"
        self.player2.name = "Joueur 2"
        self.frame1 = Frame(self.master, borderwidth=2, relief=GROOVE)
        self.frame2 = Frame(self.master, borderwidth=2, relief=GROOVE)
        self.entryPlayer1 = Entry(self.frame1, width=50)
        self.entryPlayer2 = Entry(self.frame2, width=50)
        self.create_elements()

    def create_elements(self):
        self.frame1.pack(side=LEFT, padx=30, pady=30)
        self.frame2.pack(side=LEFT, padx=10, pady=10)

        Label(self.frame1, text="Player 1", anchor=CENTER).pack()
        Label(self.frame2, text="Player 2", anchor=CENTER).pack()

        self.entryPlayer1.pack()
        self.entryPlayer2.pack()

        Button(self.frame1, text="Choose color", command=self.chooseColorPlayer1, anchor=CENTER).pack()
        Button(self.frame2, text="Choose color", command=self.chooseColorPlayer2, anchor=CENTER).pack()
        Button(self.master, text="OK", command=self.validatePlayers, anchor=CENTER, width=9).place(x=320, y=220)

    def chooseColorPlayer1(self):
        if self.player1.color is not None:
            self.player1.color = colorchooser.askcolor(title="Joueur 1")[1]

    def chooseColorPlayer2(self):
        if self.player2.color is not None:
            self.player2.color = colorchooser.askcolor(title="Joueur 2")[1]

    def validatePlayers(self):
        if self.entryPlayer1.get() != "":
            self.player1.name = self.entryPlayer1.get()

        if self.entryPlayer2.get() != "":
            self.player2.name = self.entryPlayer2.get()

        self.master.destroy()
        root = Tk()
        Game(root, self.player1, self.player2)
        root.mainloop()


class Game:
    def __init__(self, master, p1, p2):
        self.master = master
        self.master.title("Puissance 4")
        self.lines = 7
        self.columns = 6
        self.overlap = 110
        self.gameTab = np.zeros((self.lines, self.columns))
        self.player = random.randint(1, 2)
        self.player1 = p1
        self.player2 = p2
        self.game = True
        self.canvas = Canvas(self.master, width=655, height=765, background='darkblue')
        self.text = StringVar()
        self.text.set("Test")
        self.infoPlayer = Label(self.master, text=self.text, bg="yellow")
        self.currentPlayer = self.player1.name
        if self.player == 1:
            self.currentPlayer = self.player1
        else:
            self.currentPlayer = self.player2
        self.changeText(self.currentPlayer)
        self.create_element()

    def changeText(self, player):
        self.infoPlayer.configure(text=str(player.name) + ", it's your turn")
        self.infoPlayer.configure(bg=player.color)

    def create_element(self):
        self.canvas.bind('<Button-1>', self.getCoordinates)

        self.canvas.pack()

        # Draw circles
        for i in range(0, self.columns):
            for j in range(0, self.lines):
                drawCircle(self.canvas, i, j, self.overlap)

        self.infoPlayer.pack()

        button = Button(self.master, text="Replay", command=self.reinitialise)
        button.pack()

    def fall(self, y):
        x = self.lines - 1
        while self.gameTab[x][y] != 0 and x >= 0:
            x -= 1

        if x >= 0:
            return x
        return -1

    def isFull(self):
        return 0 not in self.gameTab

    def win(self, player):
        # lines
        for x in range(0, self.lines):
            for y in range(0, self.columns - 4 + 1):
                if self.gameTab[x][y] == player and self.gameTab[x][y + 1] == player and self.gameTab[x][
                    y + 2] == player and \
                        self.gameTab[x][y + 3] == self.player:
                    return True

        # columns
        for y in range(0, self.columns):
            for x in range(0, self.lines - 4 + 1):
                if self.gameTab[x][y] == player and self.gameTab[x + 1][y] == player and self.gameTab[x + 2][
                    y] == player and \
                        self.gameTab[x + 3][y] == self.player:
                    return True

        # Diagonals
        for x in range(self.lines - 4, self.lines):
            for y in range(0, self.columns - 4 + 1):
                if (self.gameTab[x][y] == player and self.gameTab[x - 1][y + 1] == player and
                        self.gameTab[x - 2][y + 2] == player and
                        self.gameTab[x - 3][y + 3] == player):
                    return True

        for x in range(self.lines - 4, self.lines):
            for y in range(self.columns - 4 + 1, self.columns):
                if (self.gameTab[x][y] == player and self.gameTab[x - 1][y - 1] == player and
                        self.gameTab[x - 2][y - 2] == player and
                        self.gameTab[x - 3][y - 3] == player):
                    return True

        return False

    def getCoordinates(self, event):
        y = (event.y - 10) / self.overlap

        if self.game:
            if self.player == 1:
                color = self.player1.color
                namePlayer = self.player1.name
                self.currentPlayer = self.player2
            else:
                color = self.player2.color
                namePlayer = self.player2.name
                self.currentPlayer = self.player1
            self.changeText(self.currentPlayer)
            y = (event.x - 10) / self.overlap
            y = int(y)
            x = self.fall(y)
            if x == -1:
                showwarning(title="Warning", message="This column is full")
            else:
                self.canvas.create_oval(10 + (self.overlap * y), 10 + (self.overlap * x),
                                        100 + (self.overlap * y), 100 + (self.overlap * x),
                                        fill=color)

                self.gameTab[x][y] = self.player

                if self.win(self.player):
                    self.game = False
                    if showinfo(title="info", message=namePlayer + " wins"):
                        self.reinitialise()
                elif self.isFull():
                    self.game = False
                    if showinfo(title="info", message="Nobody wins"):
                        self.reinitialise()
                if self.player == 1:
                    self.player = 2
                else:
                    self.player = 1

    def reinitialise(self):
        self.lines = 7
        self.columns = 6
        self.overlap = 110
        self.gameTab = np.zeros((self.lines, self.columns))
        self.player = random.randint(1, 2)
        if self.player == 1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1
        self.changeText(self.currentPlayer)
        self.game = True

        for i in range(0, self.columns):
            for j in range(0, self.lines):
                drawCircle(self.canvas, i, j, self.overlap)


def main():
    root = Tk()
    WindowInfoPlayers(root)
    root.mainloop()


if __name__ == '__main__':
    main()

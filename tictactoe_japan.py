import math
import random
import tkinter as tk


class SakuraTicTacToe:

  def __init__(self, root):
    self.root = root
    self.root.title("Sakura Garden Tic Tac Toe")

    # Start in Full Screen Mode
    self.is_fullscreen = True
    self.root.attributes("-fullscreen", True)

    # Bind keys: ESC to exit full screen, F11 to toggle
    self.root.bind("<Escape>", self.exit_fullscreen)
    self.root.bind("<F11>", self.toggle_fullscreen)

    # State: "SELECTING" or "PLAYING"
    self.state = "SELECTING"
    self.player_symbol = "X"
    self.current_player = "X"
    self.board = [["" for _ in range(3)] for _ in range(3)]
    self.game_over = False
    self.announcement_text = ""
    self.announcement_color = "#AD1457"

    # Initialize falling petals for animation
    self.petals = []
    for _ in range(35):
      self.petals.append({
          "x": random.randint(0, 1200),
          "y": random.randint(0, 800),
          "speed": random.uniform(1.5, 4.0),
          "size": random.uniform(8, 16),
          "drift": random.uniform(-0.8, 0.8),
      })

    self.create_widgets()

    # Start the animation loop (updates every 35ms)
    self.animate()

  def create_widgets(self):
    self.canvas = tk.Canvas(self.root, highlightthickness=0)
    self.canvas.pack(fill="both", expand=True)
    self.canvas.bind("<Button-1>", self.handle_click)

  def exit_fullscreen(self, event=None):
    self.is_fullscreen = False
    self.root.attributes("-fullscreen", False)
    self.root.geometry("1000x700")

  def toggle_fullscreen(self, event=None):
    self.is_fullscreen = not self.is_fullscreen
    self.root.attributes("-fullscreen", self.is_fullscreen)

  def animate(self):
    w = self.root.winfo_width()
    h = self.root.winfo_height()

    if w > 1 and h > 1:
      # Update falling petals positions
      for p in self.petals:
        p["y"] += p["speed"]
        p["x"] += p["drift"] + math.sin(p["y"] * 0.02) * 0.5

        if p["y"] > h:
          p["y"] = -10
          p["x"] = random.randint(0, w)
        if p["x"] > w:
          p["x"] = 0
        elif p["x"] < 0:
          p["x"] = w

      self.draw_all(w, h)

    self.root.after(35, self.animate)

  def draw_all(self, w, h):
    self.canvas.delete("all")

    # 1. Background Japanese Blossom Environment
    self.draw_japanese_background(w, h)

    # Helper instruction
    self.canvas.create_text(
        w / 2,
        h * 0.95,
        text="Press [ESC] to exit full screen | [F11] to toggle full screen",
        font=("Helvetica", 10, "italic"),
        fill="#555555",
    )

    if self.state == "SELECTING":
      self.draw_team_selection(w, h)
    else:
      self.draw_game_board(w, h)

  def draw_team_selection(self, w, h):
    # Title
    self.canvas.create_text(
        w / 2,
        h * 0.25,
        text="🌸 Sakura Garden Tic Tac Toe 🌸",
        font=("Helvetica", int(h * 0.045), "bold"),
        fill="#880E4F",
    )
    self.canvas.create_text(
        w / 2,
        h * 0.33,
        text="Choose Your Side",
        font=("Helvetica", int(h * 0.03), "bold"),
        fill="#AD1457",
    )

    # Button dimensions
    bw, bh = int(w * 0.18), int(h * 0.12)
    by = h * 0.48

    # Button X coordinates
    self.btn_x_x1 = w * 0.32 - bw / 2
    self.btn_x_x2 = self.btn_x_x1 + bw
    self.btn_x_y1 = by
    self.btn_x_y2 = by + bh

    # Button O coordinates
    self.btn_o_x1 = w * 0.68 - bw / 2
    self.btn_o_x2 = self.btn_o_x1 + bw
    self.btn_o_y1 = by
    self.btn_o_y2 = by + bh

    # Draw Button X
    self.canvas.create_rectangle(
        self.btn_x_x1,
        self.btn_x_y1,
        self.btn_x_x2,
        self.btn_x_y2,
        fill="#FFFAFA",
        outline="#D81B60",
        width=4,
    )
    self.canvas.create_text(
        w * 0.32,
        by + bh / 2,
        text="Play as X",
        font=("Helvetica", int(bh * 0.35), "bold"),
        fill="#D81B60",
    )

    # Draw Button O
    self.canvas.create_rectangle(
        self.btn_o_x1,
        self.btn_o_y1,
        self.btn_o_x2,
        self.btn_o_y2,
        fill="#FFFAFA",
        outline="#1E88E5",
        width=4,
    )
    self.canvas.create_text(
        w * 0.68,
        by + bh / 2,
        text="Play as O",
        font=("Helvetica", int(bh * 0.35), "bold"),
        fill="#1E88E5",
    )

  def draw_game_board(self, w, h):
    # Header Texts
    title_size = max(18, int(h * 0.035))
    status_size = max(14, int(h * 0.025))

    self.canvas.create_text(
        w / 2,
        h * 0.06,
        text="🌸 Sakura Garden Tic Tac Toe 🌸",
        font=("Helvetica", title_size, "bold"),
        fill="#880E4F",
    )

    if not self.game_over:
      status_msg = f"Current Turn: Player {self.current_player} (You are {self.player_symbol})"
    else:
      status_msg = self.announcement_text

    self.canvas.create_text(
        w / 2,
        h * 0.12,
        text=status_msg,
        font=("Helvetica", status_size, "bold"),
        fill=self.announcement_color,
    )

    # Draw Game Board
    board_size = min(w * 0.5, h * 0.55)
    self.board_x = (w - board_size) / 2
    self.board_y = (h - board_size) / 2 + (h * 0.03)
    self.board_size = board_size

    # Wooden frame background
    self.canvas.create_rectangle(
        self.board_x - 10,
        self.board_y - 10,
        self.board_x + board_size + 10,
        self.board_y + board_size + 10,
        fill="#3E2723",
        outline="#1B0000",
        width=4,
    )

    cell_size = board_size / 3
    self.cell_size = cell_size

    # Draw Cells and Markers
    for r in range(3):
      for c in range(3):
        x1 = self.board_x + c * cell_size
        y1 = self.board_y + r * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size

        self.canvas.create_rectangle(
            x1 + 3,
            y1 + 3,
            x2 - 3,
            y2 - 3,
            fill="#FFFAFA",
            outline="#D7CCC8",
            width=2,
        )

        val = self.board[r][c]
        if val:
          color = "#D81B60" if val == "X" else "#1E88E5"
          self.canvas.create_text(
              (x1 + x2) / 2,
              (y1 + y2) / 2,
              text=val,
              font=("Helvetica", int(cell_size * 0.5), "bold"),
              fill=color,
          )

    # Flashy Over-the-Screen Message if Game Over
    if self.game_over:
      self.canvas.create_rectangle(
          self.board_x,
          self.board_y + board_size * 0.35,
          self.board_x + board_size,
          self.board_y + board_size * 0.65,
          fill="#FFF0F5",
          outline=self.announcement_color,
          width=4,
      )
      self.canvas.create_text(
          w / 2,
          self.board_y + board_size * 0.5,
          text=self.announcement_text,
          font=("Impact", int(board_size * 0.08), "bold"),
          fill=self.announcement_color,
      )

    # Reset Button at bottom center
    self.btn_w, self.btn_h = 160, 40
    self.btn_x = (w - self.btn_w) / 2
    self.btn_y = self.board_y + board_size + (h * 0.04)

    self.canvas.create_rectangle(
        self.btn_x,
        self.btn_y,
        self.btn_x + self.btn_w,
        self.btn_y + self.btn_h,
        fill="#C2185B",
        outline="#880E4F",
        width=2,
    )
    self.canvas.create_text(
        self.btn_x + self.btn_w / 2,
        self.btn_y + self.btn_h / 2,
        text="Main Menu",
        font=("Helvetica", 12, "bold"),
        fill="white",
    )

  def draw_japanese_background(self, w, h):
    # Sky
    self.canvas.create_rectangle(0, 0, w, h, fill="#FFF5F7", outline="")

    # Distant Lavender Mountains
    self.canvas.create_polygon(
        0,
        h * 0.7,
        w * 0.25,
        h * 0.45,
        w * 0.5,
        h * 0.65,
        w * 0.8,
        h * 0.4,
        w,
        h * 0.75,
        w,
        h,
        0,
        h,
        fill="#E8D7F1",
        outline="",
    )

    # Red Sun (Hinomaru)
    sun_r = min(w, h) * 0.12
    self.canvas.create_oval(
        w * 0.75 - sun_r,
        h * 0.2 - sun_r,
        w * 0.75 + sun_r,
        h * 0.2 + sun_r,
        fill="#FFCDD2",
        outline="",
    )

    # Cherry Blossom Branch (Top-Left)
    self.canvas.create_arc(
        -w * 0.1,
        -h * 0.1,
        w * 0.4,
        h * 0.4,
        start=270,
        extent=90,
        style="arc",
        outline="#4E342E",
        width=max(4, int(w * 0.01)),
    )
    self.canvas.create_arc(
        w * 0.05,
        h * 0.05,
        w * 0.5,
        h * 0.5,
        start=180,
        extent=90,
        style="arc",
        outline="#4E342E",
        width=max(2, int(w * 0.006)),
    )

    # Render Animated Falling Petals
    for p in self.petals:
      px, py, size = p["x"], p["y"], p["size"]
      self.canvas.create_oval(
          px, py, px + size, py + size * 0.6, fill="#FFB7C5", outline=""
      )
      self.canvas.create_oval(
          px + size * 0.3,
          py - size * 0.2,
          px + size * 1.3,
          py + size * 0.4,
          fill="#FFC0CB",
          outline="",
      )

  def handle_click(self, event):
    mx, my = event.x, event.y

    if self.state == "SELECTING":
      # Check if user clicked Play as X or Play as O
      if (
          self.btn_x_x1 <= mx <= self.btn_x_x2
          and self.btn_x_y1 <= my <= self.btn_x_y2
      ):
        self.player_symbol = "X"
        self.state = "PLAYING"
        self.reset_game()
      elif (
          self.btn_o_x1 <= mx <= self.btn_o_x2
          and self.btn_o_y1 <= my <= self.btn_o_y2
      ):
        self.player_symbol = "O"
        self.state = "PLAYING"
        self.reset_game()

    elif self.state == "PLAYING":
      # Check if Main Menu button was clicked
      if (
          self.btn_x <= mx <= self.btn_x + self.btn_w
          and self.btn_y <= my <= self.btn_y + self.btn_h
      ):
        self.state = "SELECTING"
        return

      # Check if Board was clicked
      if not self.game_over:
        for r in range(3):
          for c in range(3):
            x1 = self.board_x + c * self.cell_size
            y1 = self.board_y + r * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size

            if x1 <= mx <= x2 and y1 <= my <= y2:
              if self.board[r][c] == "":
                self.board[r][c] = self.current_player
                self.check_game_state()
                if not self.game_over:
                  self.current_player = (
                      "O" if self.current_player == "X" else "X"
                  )

  def check_game_state(self):
    winner = None

    for r in range(3):
      if (
          self.board[r][0] == self.board[r][1] == self.board[r][2]
          and self.board[r][0] != ""
      ):
        winner = self.board[r][0]

    for c in range(3):
      if (
          self.board[0][c] == self.board[1][c] == self.board[2][c]
          and self.board[0][c] != ""
      ):
        winner = self.board[0][c]

    if (
        self.board[0][0] == self.board[1][1] == self.board[2][2]
        and self.board[0][0] != ""
    ):
      winner = self.board[0][0]
    if (
        self.board[0][2] == self.board[1][1] == self.board[2][0]
        and self.board[0][2] != ""
    ):
      winner = self.board[0][2]

    if winner:
      self.game_over = True
      loser = "O" if winner == "X" else "X"
      self.announcement_text = f"LOSER {loser}! L2P!"
      self.announcement_color = "#D32F2F"
      return

    if all(self.board[r][c] != "" for r in range(3) for c in range(3)):
      self.game_over = True
      self.announcement_text = "⚡ DRAW! GARDEN RESTS ⚡"
      self.announcement_color = "#E65100"

  def reset_game(self):
    self.current_player = "X"
    self.board = [["" for _ in range(3)] for _ in range(3)]
    self.game_over = False
    self.announcement_text = ""
    self.announcement_color = "#AD1457"


if __name__ == "__main__":
  root = tk.Tk()
  app = SakuraTicTacToe(root)
  root.mainloop()
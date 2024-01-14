#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by Zakk Loveall
With supplementary code by Dr. Shukla
"""
#-------------------------------------------------------------------------
# Tac-Tac-Tical
# This program is designed to play Tic-Tac-Tical, using lookahead and board heuristics.
# It will allow the user to play a game against the machine, or allow the machine
# to play against itself for purposes of learning to improve its play.  All 'learning'
# code has been removed from this program.
#
# Tic-Tac-Tical is a 2-player game played on a grid. Each player has the same number
# of tokens distributed on the grid in an initial configuration.  On each turn, a player
# may move one of his/her tokens one unit either horizontally or vertically (not
# diagonally) into an unoccupied square.  The objective is to be the first player to get
# three tokens in a row, either horizontally, vertically, or diagonally.
#
# The board is represented by a matrix with extra rows and columns forming a
# boundary to the playing grid. Squares in the playing grid can be occupied by
# either 'X', 'O', or 'Empty' spaces.  The extra elements are filled with 'Out of Bounds'
# squares, which makes some of the computations simpler.
#-------------------------------------------------------------------------

from __future__ import print_function
import random
from random import randrange
import copy
import time


pruned = 0
total_checked = 0
total_depth = 0
times = []

def GetMoves (Player, Board):
#-------------------------------------------------------------------------
# Determines all legal moves for Player with current Board,
# and returns them in MoveList.
#-------------------------------------------------------------------------

  MoveList = []
  for i in range(1,NumRows+1):
    for j in range(1,NumCols+1):
      if Board[i][j] == Player:
      #-------------------------------------------------------------
      #  Check move directions (m,n) = (-1,0), (0,-1), (0,1), (1,0)
      #-------------------------------------------------------------
        for m in range(-1,2):
          for n in range(-1,2):
            if abs(m) != abs(n):
              if Board[i + m][j + n] == Empty:
                MoveList.append([i, j, i+m, j+n])

  return MoveList


def GetHumanMove (Player, Board):
#-------------------------------------------------------------------------
# If the opponent is a human, the user is prompted to input a legal move.
# Determine the set of all legal moves, then check input move against it.
#-------------------------------------------------------------------------
  MoveList = GetMoves(Player, Board)
  Move = None

  while(True):
    FromRow, FromCol, ToRow, ToCol = map(int, \
      input('Input your move (FromRow, FromCol, ToRow, ToCol): ').split(' '))

    ValidMove = False
    if not ValidMove:
      for move in MoveList:
        if move == [FromRow, FromCol, ToRow, ToCol]:
          ValidMove = True
          Move = move

    if ValidMove:
      break

    print('Invalid move.  ')

  return Move


def ApplyMove (Board, Move):
#-------------------------------------------------------------------------
# Perform the given move, and update Board.
#-------------------------------------------------------------------------

  FromRow, FromCol, ToRow, ToCol = Move
  newBoard = copy.deepcopy(Board)
  Board[ToRow][ToCol] = Board[FromRow][FromCol]
  Board[FromRow][FromCol] = Empty
  return Board


def InitBoard (Board):
#-------------------------------------------------------------------------
# Initialize the game board.
#-------------------------------------------------------------------------

  for i in range(0,BoardRows+1):
    for j in range(0,BoardCols+1):
      Board[i][j] = OutOfBounds

  for i in range(1,NumRows+1):
    for j in range(1,NumCols+1):
      Board[i][j] = Empty

  for j in range(1,NumCols+1):
    if odd(j):
      Board[1][j] = x
      Board[NumRows][j] = o
    else:
      Board[1][j] = o
      Board[NumRows][j] = x


def odd(n):
  return n%2==1

def ShowBoard (Board):
  print("")
  row_divider = "+" + "-"*(NumCols*4-1) + "+"
  print(row_divider)

  for i in range(1,NumRows+1):
    for j in range(1,NumCols+1):
      if Board[i][j] == x:
        print('| X ',end="")
      elif Board[i][j] == o:
        print('| O ',end="")
      elif Board[i][j] == Empty:
        print('|   ',end="")
    print('|')
    print(row_divider)

  print("")


def Win (Player, Board):
  for i in range(1,NumRows+1):
    for j in range(1,NumCols+1):
      if Board[i][j] == Player and Board[i+1][j] == Player and Board[i+2][j] == Player:
        return True
      if Board[i][j] == Player and Board[i][j+1] == Player and Board[i][j+2] == Player:
        return True
      if Board[i][j] == Player and Board[i+1][j+1] == Player and Board[i+2][j+2] == Player:
        return True
  return False

def GetComputerMove(Player, Board):
  global times
  start = time.time()
  moves = GetMoves(Player, Board)
  best_move = None
  new_value = -infinity
  for i in moves:
    temp_board = copy.deepcopy(Board)
    copy_board = ApplyMove(temp_board, i)
    value = ab_minimax(Player, copy_board, MaxDepth, -infinity, infinity, False)
    if value > new_value:
      new_value = value
      best_move = i
  print(f"Computer made move to {best_move}, which scored {new_value}")
  end = time.time()
  times.append(end-start)
  return best_move
    
def userid_h(Player, Board):
  computer_score = 0
  player_score = 0
  if (Player == x):
    if (Win(Player,Board) == True):
      player_score = infinity
    else:
      for i in range(1,NumRows+1):
        for j in range(1,NumCols+1):
          if (Board[i][j] == o and Board[i+1][j] == o and Board[i+2][j] == x) or (Board[i][j] == x and Board[i+1][j] == o and Board[i+2][j] == o) or (Board[i][j] == o and Board[i+1][j] == x and Board[i+2][j] == o):
            player_score += 8
            
          elif (Board[i][j] == o and Board[i][j+1] == o and Board[i][j+2] == x) or (Board[i][j] == x and Board[i][j+1] == o and Board[i][j+2] == o) or (Board[i][j] == o and Board[i][j+1] == x and Board[i][j+2] == o):
            player_score += 8
            
          elif (Board[i][j] == o and Board[i+1][j+1] == o and Board[i+2][j+2] == x) or (Board[i][j] == x and Board[i+1][j+1] == o and Board[i+2][j+2] == o) or (Board[i][j] == o and Board[i+1][j+1] == x and Board[i+2][j+2] == o):
            player_score += 8
            
          elif (Board[i][j] == x and Board[i+1][j] == x and Board[i+2][j] == Empty) or (Board[i][j] == x and Board[i+1][j] == Empty and Board[i+2][j] == x) or (Board[i][j] == Empty and Board[i+1][j] == x and Board[i+2][j] == x):
            player_score += 3
            
          elif (Board[i][j] == x and Board[i][j+1] == x and Board[i][j+2] == Empty) or (Board[i][j] == x and Board[i][j+1] == Empty and Board[i][j+2] == x) or (Board[i][j] == Empty and Board[i][j+1] == x and Board[i][j+2] == x):
            player_score += 3
            
          elif (Board[i][j] == x and Board[i+1][j+1] == x and Board[i+2][j+2] == Empty) or (Board[i][j] == x and Board[i+1][j+1] == Empty and Board[i+2][j+2] == x) or (Board[i][j] == Empty and Board[i+1][j+1] == x and Board[i+2][j+2] == x):
            player_score += 3
            
          else:
            player_score += 1
  elif Player == o:
    if (Win(Player,Board) == True):
      computer_score = -infinity
    else:
      for i in range(1,NumRows+1):
        for j in range(1,NumCols+1):
          if (Board[i][j] == x and Board[i+1][j] == x and Board[i+2][j] == o) or (Board[i][j] == o and Board[i+1][j] == x and Board[i+2][j] == x) or (Board[i][j] == x and Board[i+1][j] == o and Board[i+2][j] == x):
            computer_score += 8
            
          elif (Board[i][j] == x and Board[i][j+1] == x and Board[i][j+2] == o) or (Board[i][j] == o and Board[i][j+1] == x and Board[i][j+2] == x) or (Board[i][j] == x and Board[i][j+1] == o and Board[i][j+2] == x):
            computer_score += 8
            
          elif (Board[i][j] == x and Board[i+1][j+1] == x and Board[i+2][j+2] == o) or (Board[i][j] == o and Board[i+1][j+1] == x and Board[i+2][j+2] == x) or (Board[i][j] == x and Board[i+1][j+1] == o and Board[i+2][j+2] == x):
            computer_score += 8
            
          elif (Board[i][j] == o and Board[i+1][j] == o and Board[i+2][j] == Empty) or (Board[i][j] == o and Board[i+1][j] == Empty and Board[i+2][j] == o) or (Board[i][j] == Empty and Board[i+1][j] == o and Board[i+2][j] == o):
            computer_score += 3
            
          elif (Board[i][j] == o and Board[i][j+1] == o and Board[i][j+2] == Empty) or (Board[i][j] == o and Board[i][j+1] == Empty and Board[i][j+2] == o) or (Board[i][j] == Empty and Board[i][j+1] == o and Board[i][j+2] == o):
            computer_score += 3
            
          elif (Board[i][j] == o and Board[i+1][j+1] == o and Board[i+2][j+2] == Empty) or (Board[i][j] == o and Board[i+1][j+1] == Empty and Board[i+2][j+2] == o) or (Board[i][j] == Empty and Board[i+1][j+1] == o and Board[i+2][j+2] == o):
            computer_score += 3
            
          else:
            computer_score += 1
          
  return computer_score - player_score

def ab_minimax(player, Board, depth, alpha, beta, maxer):
  global total_checked
  global pruned
  global total_depth
  total_checked += 1
  if depth == 0 or Win(player, Board) == True:
    return userid_h(player, Board)

  if maxer:
    max_eval = -infinity
    moves = GetMoves(o, Board)
    total_depth += 1
    for i in moves:
      temp_board = copy.deepcopy(Board)
      new_board = ApplyMove(temp_board, i)
      eval = ab_minimax(player, new_board, depth - 1, alpha, beta, False)
      max_eval = max(max_eval, eval)
      alpha = max(alpha, eval)
      if beta <= alpha:
        pruned += 1
        break
    return max_eval
  else:
    min_eval = infinity
    moves = GetMoves(x, Board)
    total_depth += 1
    for i in moves:
      temp_board = copy.deepcopy(Board)
      new_board = ApplyMove(temp_board, i)
      eval = ab_minimax(player, new_board, depth - 1, alpha, beta, True)
      min_eval = min(min_eval, eval)
      beta = min(beta, eval)
      if beta <= alpha:
        pruned += 1
        break 
    return min_eval



if __name__ == "__main__":
#-------------------------------------------------------------------------
# A move is represented by a list of 4 elements, representing 2 pairs of
# coordinates, (FromRow, FromCol) and (ToRow, ToCol), which represent the
# positions of the piece to be moved, before and after the move.
#-------------------------------------------------------------------------
  x = -1
  o = 1
  Empty = 0
  OutOfBounds = 2
  NumRows = 5
  BoardRows = NumRows + 1
  NumCols = 4
  BoardCols = NumCols + 1
  MaxMoves = 4*NumCols
  NumInPackedBoard = 4 * (BoardRows+1) *(BoardCols+1)
  infinity = 10000  # Value of a winning board
  MaxDepth = 4
  Board = [[0 for col in range(BoardCols+1)] for row in range(BoardRows+1)]

  player_piece = x
  computer_piece = o
  first_move = random.randint(0,1)
  selection = int(input("If you want the computer to play against itself, enter 0, else enter 1"))
  
  if (selection != 0):
    print("\nThe squares of the board are numbered by row and column, with '1 1' ")
    print("in the upper left corner, '1 2' directly to the right of '1 1', etc.")
    print("")
    print("Moves are of the form 'i j m n', where (i,j) is a square occupied")
    print("by your piece, and (m,n) is the square to which you move it.")
    print("")
    player_piece = random.randint(0,1)
    if (player_piece == 0):
      player_piece = x
      computer_piece = o
      print("You move the 'X' pieces.\n")
    else:
      player_piece = o
      computer_piece = x
      print("You move the '0' pieces.\n")
  else:
    print("Computer will play against itself!")

  InitBoard(Board)
  ShowBoard(Board)

  MoveList = GetMoves(x,Board)
  print(MoveList)
  MoveList = GetMoves(o,Board)
  print(MoveList)

  while True:
    if (selection != 0):
      if (first_move == 0):
        Move = GetHumanMove(player_piece,Board)
        Board = ApplyMove(Board,Move)
        ShowBoard(Board)
        if (Win(player_piece,Board) == True):
          print(f"Player {player_piece} Wins!")
          break
        Move = GetComputerMove(computer_piece,Board)
        Board = ApplyMove(Board,Move)
        ShowBoard(Board)
        if (Win(computer_piece,Board) == True):
          print(f"Player {computer_piece} Wins!")
          break
      else:
        Move = GetComputerMove(computer_piece,Board)
        Board = ApplyMove(Board,Move)
        ShowBoard(Board)
        if (Win(computer_piece,Board) == True):
          print(f"Player {computer_piece} Wins!")
          break
        Move = GetHumanMove(player_piece,Board)
        Board = ApplyMove(Board,Move)
        ShowBoard(Board)
        if (Win(player_piece,Board) == True):
          print(f"Player {player_piece} Wins!")
          break
    else:
      if (first_move == 0):
        Move = GetComputerMove(x,Board)
        Board = ApplyMove(Board,Move)
        ShowBoard(Board)
        if (Win(x,Board) == True):
          print("Player X Wins!")
          break
        Move = GetComputerMove(o,Board)
        Board = ApplyMove(Board,Move)
        ShowBoard(Board)
        if (Win(o,Board) == True):
          print("Player O Wins!")
          break
      else:
        Move = GetComputerMove(o,Board)
        Board = ApplyMove(Board,Move)
        ShowBoard(Board)
        if (Win(x,Board) == True):
          print("Player X Wins!")
          break
        Move = GetComputerMove(x,Board)
        Board = ApplyMove(Board,Move)
        ShowBoard(Board)
        if (Win(o,Board) == True):
          print("Player O Wins!")
          break
  print(f"Total Pruned Branches: {pruned}\n")
  print(f"Total Branches Checked: {total_checked}\n")
  print(f"Max Depth Reached: {total_depth}\n")
  print(f"Average Traversal Time: {sum(times) / len(times)}\n")
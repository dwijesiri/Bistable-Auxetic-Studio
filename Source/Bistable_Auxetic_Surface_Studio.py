#
# Bistable Auxetic Mechanical Studio - Developed By Dinuk Wijesiri
#
# Overview:
#
# A lightweight application to create Bistable Auxetic Surfaces.
# Programmed in pure python and includes an intuitive mix of a 
# Command Line Interface (CLI) and Graphical User Interface (GUI)
#
# Date Created: 17th of June Monday 2024
#

# --------- Imports ---------

import os as System # Basic System Commands
import pygame as RenderEngine # Used for Graphical Rendering (Efficiency)
import tkinter as WindowRender # Base for GUI Application
from tkinter import ttk as ExtensionsI # Frame for Render Canvas
import math as Math # Basic and Complex Mathematical Operations
import ctypes as WindowStatistics # Deal with Window Size and Scaling
from itertools import chain as ToolI # Managing Lists
from contextlib import suppress as ToolII # Used in File Selection Modal
from tkinter.filedialog import askopenfilename as FileOpen # File Selection Dialog #1 (Opening Files ...)
from tkinter.filedialog import asksaveasfile as FileSaveI # File Selection Dialog #2 (Saving Files - returns File Object)
from tkinter.filedialog import asksaveasfilename as FileSaveII # File Selection Dialog #3 (Saving Files - returns File Path)
import json as FileManage # Interpret .baux files as JSON
from PIL import (Image as ImageI, ImageTk as ImageII) # Image Support In MessageBox
import drawsvg as Export # Exporting to SVG
import sys as ArgumentManage # Manage Arguments (External)

# --------- Utilities (Functions) ---------

ClearEntireConsole = lambda: System.system('clear' if System.name != 'nt' else 'cls') # Clears Command Line

ClearEntireScreen = lambda Channel: Channel.fill([255, 255, 255])

UpdateScreen = lambda: RenderEngine.display.flip()

GetScreenScale = lambda: WindowStatistics.windll.shcore.GetScaleFactorForDevice(0) / 100

PolarToNormal = lambda Radius, Theta, OffSet: (OffSet[0] + Radius * Cosine(-Theta), OffSet[1] + Radius * Sine(-Theta))

TrianglePointTestI = lambda I, II, III: ((I[0]- III[0]) * (II[1] - III[1]) - (II[0] - III[0]) * (I[1] - III[1])) < 0

TrianglePointTestII = lambda I, II, III, IV: ((TrianglePointTestI(I, II, III) == TrianglePointTestI(I, III, IV)) and (TrianglePointTestI(I, III, IV) == TrianglePointTestI(I, IV, II)))

Tangent = lambda I: Math.tan(Math.radians(I))

Cosine = lambda I: Math.cos(Math.radians(I))

Sine = lambda I: Math.sin(Math.radians(I))

def WindowSize(): # Gets Size of Screen (Including Tkinter UI)

    WindowStatistics.windll.user32.SetProcessDPIAware()
        
    return (WindowStatistics.   
    windll.user32.
    GetSystemMetrics(0),
    WindowStatistics.windll.
    user32.GetSystemMetrics(1))

def LimitScreenSize(ScreenLimit): # Check if Screen is appropriate size
        
    return True if (WindowSize()[0] 
    > ScreenLimit[0] and WindowSize()[1] >
    ScreenLimit[1] and WindowSize()[0]
    < ScreenLimit[2] and WindowSize()[1] <
    ScreenLimit[3]) else False

def ValidateInput(Input):

    try:

        float(Input) # Try to convert string to float.

        return True # if Possible return True
    
    except ValueError:

        return False # Return False if ValueError
    
def ValidateTheta(Input):

    if Input == "": return True

    if ValidateInput(Input): # Check if Input is formatted correctly
        
        return True if 0 <= float(Input) <= 22.5 else False # Theta must be between 0 and 30 (Bistability Requirement)
        
    else:

        return False

def ValidateThickness(Input, CellSize):

    if Input == "": return True

    if ValidateInput(Input):

        return True if 0 <= float(Input) <= 0.3 * CellSize else False # Thickness must be less than or equal to 30% of cell size (Bistability Requirement)

    else:

        return False

class ApplicationMenu: # Tkinter Application Menu

    def __init__ (Module):

        Module.MenuRoot = (
        WindowRender.Menu(
        WindowRendering))
        WindowRendering.config(
        menu = Module.MenuRoot)
        Module.MenuRoot.config(
        activeborderwidth = 0)

    def __call__(Module, MenuBar, SubBranches, Action):

        for BranchOption in range(len(MenuBar)):

            Branch = WindowRender.Menu(
                Module.MenuRoot,
                tearoff = False,
                font = ("Bahnschrift", 8)
            )

            [Branch.add_command(
            label = SubBranches[BranchOption][_],
            command = Action[BranchOption][_]
            ) for _ in range(len(SubBranches[BranchOption]))]
            Module.MenuRoot.add_cascade(
            label = MenuBar[BranchOption],
            menu = Branch,
            underline = 0)

def ResourceLocator(InputPath): # Script Can Locate Resources across Working Directories

    try: Path = ArgumentManage._MEIPASS

    except Exception: Path = System.path.abspath(".")

    return System.path.join(Path, InputPath)

def LogoBox():

    LogoBox = WindowRender.Tk()
    LogoBox.overrideredirect(True)
    Image = ImageII.PhotoImage(ImageI.open(ResourceLocator("Logo_1.png")).resize((956, 576)))
    ImageLabel = WindowRender.Label(LogoBox, image = Image, bd = 0, highlightthickness = 0)
    ImageLabel.image = Image
    ImageLabel.pack(fill = "both", expand = True)
    LogoBox.attributes('-topmost', True)
    LogoBox.after(100, lambda: LogoBox.attributes('-topmost', False))
    LogoBox.geometry("+{}+{}".format(int(WindowSize()[0]/2 -  478), int(WindowSize()[1]/2 - 288)))
    LogoBox.resizable(False, False)
    LogoBox.after(3000, lambda: LogoBox.destroy())
    LogoBox.mainloop()
    return LogoBox

# --------- Interface Components ---------

class GridCell: # Each Component is a Single Bistable Auxetic Cell

    def __init__(Module, GridSearch, Index, Position, CellSize, Reversal = False):

        Module.Index = Index # Index in Grid
        Module.GridSearch = GridSearch # Parent Object
        Module.Data = [5, 2.5, False] # Thickness, Angle, Selected
        Module.MetaData = (CellSize, Position[0], Position[1], Reversal) # CellSize, XPosition, YPosition, Reversal

    def IsometricGrid(Module): # Basic outline of clickable Isometric Grid

        Points =  [(Module.MetaData[1] + 0.5 * Module.MetaData[0] + OffSet[0], 
        Module.MetaData[2] + (Module.MetaData[0] * (3 ** 0.5) * 0.5) * (-1 if Module.MetaData[3] else 1) + OffSet[1]),
        (Module.MetaData[1] + OffSet[0], Module.MetaData[2] + OffSet[1]),
        (Module.MetaData[1] + OffSet[0] + Module.MetaData[0], Module.MetaData[2] + OffSet[1])]
        if Module.Data[2]: RenderEngine.draw.aalines(ScreenObject, (0,0, 0), True, Points, 5) # Selected Form - Triangles
        else: [RenderEngine.draw.circle(ScreenObject, (0, 0, 0), Points[_], 2) for _ in range(3)] # Unselected Form - Circular Nodes
        Module.GridPoints = Points

    def CellAveraging(Module, Position): # Averages Thickness Values in Neighbouring cells (enables cell cuts to align)

        Result = Module.GetCells(Position) # Get Surrounding Cells
        if Result == None or Result.Data[2] == False: return Module.Data[0] # If no neighbour cell, return Cell Thickness
        else: return (Module.Data[0] + Result.Data[0]) / 2 # Otherwise average Cell Thicknesses

    def CellOutline(Module, Position):  # Outline of Grid Cell in SVG File

        Result = Module.GetCells(Position)

        if Result == None or Result.Data[2] == False:  # If no overlap of selected cells, draw outline

            if Position == 0: Module.GridSearch.ExportSVG.append(Export.Lines(Module.GridPoints[1][0], Module.GridPoints[1][1], Module.GridPoints[0][0], Module.GridPoints[0][1], fill = "none", stroke = "black"))
            elif Position == 1: Module.GridSearch.ExportSVG.append(Export.Lines(Module.GridPoints[1][0], Module.GridPoints[1][1], Module.GridPoints[2][0], Module.GridPoints[2][1], fill = "none", stroke = "black"))
            elif Position == 2: Module.GridSearch.ExportSVG.append(Export.Lines(Module.GridPoints[2][0], Module.GridPoints[2][1], Module.GridPoints[0][0], Module.GridPoints[0][1], fill = "none", stroke = "black"))

    def GetCells(Module, Position): # Gets Surrounding Grid Cell Objects (Based on Position Argument)

        if Position == 0: Result = Module.GridSearch((Module.Index[0] - 1, Module.Index[1]))
        elif Position == 1: Result = Module.GridSearch((Module.Index[0], Module.Index[1] + 1) if Module.MetaData[3] else (Module.Index[0], Module.Index[1] - 1))
        elif Position == 2: Result = Module.GridSearch((Module.Index[0] + 1, Module.Index[1])) 
        return Result

    def Auxetics(Module): # Make Auxetic cuts in isometric cell (Most memory intensive component)

        JointWidth = 3 # Width of Auxetic Hinge

        ParameterI = (((Module.MetaData[0] - (1.5 * Module.Data[0]) - (Sine(60) * Module.Data[0] / Tangent(60 - Module.Data[1]))) / (1 + (Tangent(Module.Data[1]) / Tangent(60 - Module.Data[1])))) / Cosine(Module.Data[1])) - JointWidth # Length of Each Auxetic Line (2.5 is Gap Width)

        ParameterII = ((Sine(60) * Module.Data[0]) / Sine(60 - Module.Data[1])) + ((ParameterI + JointWidth) * Sine(Module.Data[1])) / Sine(60 - Module.Data[1])

        if Module.MetaData[3]: # If Cell Is Reversed ... 

            Points = [PolarToNormal(Module.CellAveraging(0), 60, (Module.MetaData[1] + OffSet[0], Module.MetaData[2] + OffSet[1])), # (Point 1)
            PolarToNormal(ParameterII, Module.Data[1],
            PolarToNormal(Module.Data[0], 60, (Module.MetaData[1] + OffSet[0], Module.MetaData[2] + OffSet[1]))), # (Point 2)
            PolarToNormal(ParameterI, Module.Data[1], # Radius and Theta Value (Point 3)
            PolarToNormal(Module.Data[0], 60, (Module.MetaData[1] + OffSet[0], Module.MetaData[2] + OffSet[1])))] # (Point 3)

            RenderEngine.draw.aalines(ScreenObject, (255, 0, 0), False, Points, 2)

            Module.GridSearch.ExportSVG.append(Export.Lines(Points[0][0], Points[0][1], Points[1][0], Points[1][1], Points[2][0], Points[2][1], fill = "none", stroke = "black"))

            Points =  [(Module.MetaData[1] + Module.MetaData[0] - Module.CellAveraging(1) + OffSet[0], Module.MetaData[2] + OffSet[1]),
            PolarToNormal(ParameterII, 120 + Module.Data[1],
            (Module.MetaData[1] + Module.MetaData[0] - Module.Data[0] + OffSet[0], Module.MetaData[2] + OffSet[1])),
            PolarToNormal(ParameterI, 120 + Module.Data[1],
            (Module.MetaData[1] + Module.MetaData[0] - Module.Data[0] + OffSet[0], Module.MetaData[2] + OffSet[1]))]

            RenderEngine.draw.aalines(ScreenObject, (0, 0, 200), False, Points, 2)

            Module.GridSearch.ExportSVG.append(Export.Lines(Points[0][0], Points[0][1], Points[1][0], Points[1][1], Points[2][0], Points[2][1], fill = "none", stroke = "black"))

            Points = [PolarToNormal(Module.MetaData[0] - Module.CellAveraging(2), 120, (Module.MetaData[1] + Module.MetaData[0] + OffSet[0], Module.MetaData[2] + OffSet[1])),
            PolarToNormal(ParameterII, 240 + Module.Data[1], 
            PolarToNormal(Module.MetaData[0] - Module.Data[0], 120, (Module.MetaData[1] + Module.MetaData[0] + OffSet[0], Module.MetaData[2] + OffSet[1]))), 
            PolarToNormal(ParameterI, 240 + Module.Data[1], 
            PolarToNormal(Module.MetaData[0] - Module.Data[0], 120, (Module.MetaData[1] + Module.MetaData[0] + OffSet[0], Module.MetaData[2] + OffSet[1])))]

            RenderEngine.draw.aalines(ScreenObject, (195, 0, 255), False, Points, 2)

            Module.GridSearch.ExportSVG.append(Export.Lines(Points[0][0], Points[0][1], Points[1][0], Points[1][1], Points[2][0], Points[2][1], fill = "none", stroke = "black"))

        else: # If Cell is Normal ... 

            Points = [PolarToNormal(Module.CellAveraging(0), -60, (Module.MetaData[1] + OffSet[0], Module.MetaData[2] + OffSet[1])), 
            PolarToNormal(ParameterII, - Module.Data[1], 
            PolarToNormal(Module.Data[0], -60, (Module.MetaData[1] + OffSet[0], Module.MetaData[2] + OffSet[1]))),
            PolarToNormal(ParameterI, - Module.Data[1], 
            PolarToNormal(Module.Data[0], -60, (Module.MetaData[1] + OffSet[0], Module.MetaData[2] + OffSet[1])))]

            RenderEngine.draw.aalines(ScreenObject, (255, 0, 0), False, Points, 2)
            
            Module.GridSearch.ExportSVG.append(Export.Lines(Points[0][0], Points[0][1], Points[1][0], Points[1][1], Points[2][0], Points[2][1], fill = "none", stroke = "black"))

            Points = [(Module.MetaData[1] + Module.MetaData[0] - Module.CellAveraging(1) + OffSet[0], Module.MetaData[2] + OffSet[1]),
            PolarToNormal(ParameterII, 240 - Module.Data[1], 
            (Module.MetaData[1] + Module.MetaData[0] - Module.Data[0] + OffSet[0], Module.MetaData[2] + OffSet[1])),
            PolarToNormal(ParameterI, 240 - Module.Data[1], 
            (Module.MetaData[1] + Module.MetaData[0] - Module.Data[0] + OffSet[0], Module.MetaData[2] + OffSet[1]))]

            RenderEngine.draw.aalines(ScreenObject, (0, 0, 200), False, Points, 2)

            Module.GridSearch.ExportSVG.append(Export.Lines(Points[0][0], Points[0][1], Points[1][0], Points[1][1], Points[2][0], Points[2][1], fill = "none", stroke = "black"))

            Points = [PolarToNormal(Module.MetaData[0] - Module.CellAveraging(2), 240, (Module.MetaData[1] + Module.MetaData[0] + OffSet[0], Module.MetaData[2] + OffSet[1])),
            PolarToNormal(ParameterII, 120 - Module.Data[1], 
            PolarToNormal(Module.MetaData[0] - Module.Data[0], 240, (Module.MetaData[1] + Module.MetaData[0] + OffSet[0], Module.MetaData[2] + OffSet[1]))),
            PolarToNormal(ParameterI, 120 - Module.Data[1], 
            PolarToNormal(Module.MetaData[0] - Module.Data[0], 240, (Module.MetaData[1] + Module.MetaData[0] + OffSet[0], Module.MetaData[2] + OffSet[1])))]
            
            RenderEngine.draw.aalines(ScreenObject, (195, 0, 255), False, Points, 2)

            Module.GridSearch.ExportSVG.append(Export.Lines(Points[0][0], Points[0][1], Points[1][0], Points[1][1], Points[2][0], Points[2][1], fill = "none", stroke = "black"))

        [Module.CellOutline(_) for _ in range(3)] # Check Surrounding Cells and Draw SVG Outline

    def CellRendering(Module):

        Module.IsometricGrid()

        if Module.Data[2]: 
            
            Module.Auxetics()

    def ClickEvent(Module):

        Module.Data = [5, 2.5, not Module.Data[2]]

    def CellValueAdjustment(Module):

        AdjustmentWindow = WindowRender.Frame(WindowRendering)

        def CellFade(*Values):

            AdjustmentWindow.destroy()
            FrameObject.unbind_all("<Button-1>")
            FrameObject.unbind_all("<Button-3>")

        Thickness = WindowRender.StringVar(value = Module.Data[0])
        Theta = WindowRender.StringVar(value = Module.Data[1])
        ThicknessLabel = WindowRender.Label(AdjustmentWindow, text = "Width: ", font = ("Bahnschrift", 10))
        ThicknessInput = WindowRender.Entry(AdjustmentWindow, textvariable = Thickness, font = ("Bahnschrift", 10), width = 5, justify = "center", validate = "key", validatecommand = (AdjustmentWindow.register(lambda Input: ValidateThickness(Input, Module.MetaData[0])), '%P'))
        ThicknessLabel.grid(row = 1, column = 0, padx = 15)
        ThicknessInput.grid(row = 1, column = 1, ipady = 10, ipadx = 10)
        ThetaLabel = WindowRender.Label(AdjustmentWindow, text = "Theta: ", font = ("Bahnschrift", 10))
        ThetaInput = WindowRender.Entry(AdjustmentWindow, textvariable = Theta, font = ("Bahnschrift", 10), width = 5, justify = "center", validate = "key", validatecommand = (AdjustmentWindow.register(ValidateTheta), '%P'))
        ThetaLabel.grid(row = 2, column = 0, padx = 15)
        ThetaInput.grid(row = 2, column = 1, ipady = 10, ipadx = 10)
        CloseButton = WindowRender.Button(AdjustmentWindow, text="Close", command = CellFade, width = 15, highlightthickness = 0, bd = 0, font = ("Bahnschrift", 10))
        CloseButton.grid(row = 3, column = 0, columnspan = 2)
        AdjustmentWindow.update()
        AdjustmentWindow.place(
        x = WindowRendering.winfo_screenwidth() - AdjustmentWindow.winfo_reqwidth(),
        y = WindowRendering.winfo_screenheight() - AdjustmentWindow.winfo_reqheight() - CloseButton.winfo_reqheight())

        def UpdateValues(*Values):
    
            if Thickness.get() != "" and Theta.get() != "" and ValidateTheta(Theta.get()) and ValidateThickness(Thickness.get(), Module.MetaData[0]): 
                
                Module.Data[0], Module.Data[1] = float(Thickness.get()), float(Theta.get())

            Module.GridSearch.RenderGrid()

        Thickness.trace_add('write', UpdateValues)
        Theta.trace_add('write', UpdateValues)
        FrameObject.bind("<Button-1>", CellFade)
        FrameObject.bind("<Button-3>", CellFade)

    def __repr__(Module):

        return f'\nGrid Cell Object:\n\nThickness: { Module.Data[0]}\n\nAngle: {Module.Data[1]}\n'

class Grid: # Sets up Grid of GridCell objects based on preset argument or Screen Size

    def __init__(Module, GUI, CellSize = 50, Input = [], Dimension = [0, 0]):

        Module.Clock = RenderEngine.time.Clock() # Controls Frame Rate (40 FPS)
        Module.GUI = GUI
        Module.RunProgram = True
        Module.Dimension = Dimension if bool(Dimension[0]) and bool(Dimension[1]) else [
        int(WindowSize()[0] / CellSize) + 1,
        int(WindowSize()[1] // (Math.sqrt( 3 * (CellSize ** 2) / 4)) + 1)]
        Module.CellSize = CellSize
        Module.ExportSVG = Export.Drawing(Module.GUI.ScreenDimensions[0], Module.GUI.ScreenDimensions[1], origin = (0, 0))

        Module.Grid = [
            
        [(GridCell(Module, # Parent Grid Object
        (2 * XDimension + 1 if # Index Calculation
        bool(YDimension % 2) else 
        2 * XDimension, YDimension + 1),
        ((XDimension * Module.CellSize + (YDimension % 2) * (Module.CellSize / 2)) - 0.5 * CellSize,
        (YDimension * Math.sqrt(3 * (Module.CellSize ** 2) / 4))), #Calculate Position
        Module.CellSize, # Size of Isometric Cell
        Reversal = False), # Type of Cell (Reversed or Normal)

        GridCell(Module,
        (2 * XDimension + 1 if
        bool(YDimension % 2) else
        2 * XDimension, YDimension), 
        ((XDimension * Module.CellSize + (YDimension % 2) * (Module.CellSize / 2)) - 0.5 * CellSize,
        (YDimension * Math.sqrt(3 * (Module.CellSize ** 2) / 4))), 
        Module.CellSize, 
        Reversal = True))

        for XDimension in range(Module.Dimension[0])] # loops over Each Row
        
        for YDimension in range(Module.Dimension[1])] # Loops over Each Column

        Grid = [[None for _ in range(2 * Module.Dimension[0])] for _ in range(Module.Dimension[1] + 1)]
        
        Module.Grid = list(ToolI(*[ # Reorganizing grid so that it can be efficiently indexed into.
        [XPosition[0] 
        for XPosition in YPosition]
        for YPosition in Module.Grid]
        + [[XPosition[1] for XPosition in YPosition]
        for YPosition in Module.Grid]))

        for Cell in Module.Grid: 

            Grid[Cell.Index[1]][Cell.Index[0]] = Cell

        Module.Grid = Grid

        for Inputs in Input: 
            
            if Module(Inputs[0]) != None: 
                
                Module(Inputs[0]).Data[2] = True # Loops through Inputs and applies existing Data
                Module(Inputs[0]).Data[0] = Inputs[1]
                Module(Inputs[0]).Data[1] = Inputs[2]

        Module.RenderLoop()

    def __call__(Module, Input): # Same Structure as Module.UpdateGrid() Function

        if 0 <= Input[0] < 2 * Module.Dimension[0] and 0 <= Input[1] < Module.Dimension[1]:

            return Module.Grid[Input[1]][Input[0]]

        return None

    def RenderLoop(Module):
        
        if RenderEngine.time.get_ticks() < 1000: 

            ClearEntireScreen(ScreenObject)

            Module.ExportSVG = Export.Drawing(
                Module.GUI.ScreenDimensions[0],
                Module.GUI.ScreenDimensions[1],
                origin = (0, 0))
            
        Module.Clock.tick(40) # Limit Frame Rate to 40 FPS
        RenderEngine.draw.rect(ScreenObject, # Drawing Border for Grid
        (0, 0, 0),
        (OffSet[0] - 0.5 * Module.CellSize, OffSet[1] - Math.sqrt(3 * Module.CellSize ** 2 / 4), # Grid Moves With Offset
        Module.CellSize * (Module.Dimension[0] + 0.5), 
        Math.sqrt(3 * Module.CellSize ** 2 / 4) * (Module.Dimension[1] + 1)), 1, 5)
        if RenderEngine.time.get_ticks() < 1000: Module.RenderGrid()
        Module.HandleEventListeners()
        UpdateScreen()
        if Module.RunProgram: WindowRendering.after(20, Module.RenderLoop) # Theoretical Frame Rate of 50 FPS
        else: ClearEntireScreen(ScreenObject)

    def RenderGrid(Module):

        ClearEntireScreen(ScreenObject)

        Module.ExportSVG = Export.Drawing(
            Module.GUI.ScreenDimensions[0],
            Module.GUI.ScreenDimensions[1],
            origin = (0, 0))
        
        [[XPosition.CellRendering() if XPosition != None else None
        for XPosition in YPosition] for YPosition in Module.Grid]

    def HandleEventListeners(Module):

        Module.EventLog = RenderEngine.event.get(pump = False) # Get All Event Listeners (Use Pump = False to Avoid GIL Error)

        for _ in Module.EventLog: # Loop through and process triggered Events
            
            if _.type == RenderEngine.QUIT: 

                Module.RunProgram = False # End Process
                
                RenderEngine.quit() # Ends process on quitting application.

            elif _.type == RenderEngine.MOUSEBUTTONDOWN:

                if _.button == 1:

                    for YPosition in Module.Grid:

                        for XPosition in YPosition:

                            if XPosition != None:

                                XPosition.ClickEvent() if TrianglePointTestII(_.pos, *(XPosition.GridPoints)) else None

                elif _.button == 3:

                    for YPosition in Module.Grid:

                        for XPosition in YPosition:

                            if XPosition != None:

                                XPosition.CellValueAdjustment() if TrianglePointTestII(_.pos, *(XPosition.GridPoints)) and XPosition.Data[2] else None

                elif _.button == 4: # Scrolling Up

                    Module.GUI.AdjustOffset([0, 4])

                elif _.button == 5: # Scrolling Down

                    Module.GUI.AdjustOffset([0, -4])

                RenderEngine.event.pump() # Update Events and Process Queue

                Module.RenderGrid()

# --------- Graphical Interface ---------

class StudioGraphicalElementI:

    def __init__(Module, Arguments):

        Module.ScreenDimensions = [WindowSize()[0], WindowSize()[1]]
        
        Module.Arguments = Arguments

        LogoBox()

        Module.CreateGUIWindow()

        Module.Menu = ApplicationMenu()

        Module.Menu([
        "File"], [
        ["Save As", "Import",
        "Reset", "Export",
        "Exit"]], [[
        Module.Save, Module.Import, 
        Module.Reset, Module.Export,
        Module.Exit]])

        Module.StudioApplication = Grid(Module, Arguments[0], Dimension = [0, 0])

        if len(ArgumentManage.argv) > 1: Module.Import(Name = ArgumentManage.argv[1]) # Support for opening .baux file type.

        WindowRendering.mainloop()

    def CreateGUIWindow(Module): # Setting Up Tkinter and Pygame

        global WindowRendering, FrameObject, ScreenObject, OffSet
        WindowRendering = WindowRender.Tk()
        WindowRendering.title("Bistable Auxetic Surface Studio")
        WindowRendering.attributes("-fullscreen", True) # Sets window to FullScreen
        Module.Clock = RenderEngine.time.Clock()
        FrameObject = ExtensionsI.Frame(
        WindowRendering,
        width = Module.ScreenDimensions[0],
        height = Module.ScreenDimensions[1])
        FrameObject.pack(fill = "both", expand = True)
        OffSet = [0, 0] # Offset of Canvas
        System.environ['SDL_WINDOWID'] = str(FrameObject.winfo_id())
        System.environ['SDL_VIDEODRIVER'] = 'windib'
        RenderEngine.display.init() # Initalizes Rendering Engine
        ScreenObject = RenderEngine.display.set_mode(Module.ScreenDimensions, RenderEngine.FULLSCREEN | RenderEngine.DOUBLEBUF | RenderEngine.NOFRAME)
        ScreenObject.set_alpha(None)
        WindowRendering.bind('<Left>', lambda I: Module.AdjustOffset([2, 0])) # Keyoard Event Listener
        WindowRendering.bind('<Right>', lambda I: Module.AdjustOffset([-2, 0])) # Binds to arrowkeys
        WindowRendering.bind('<Up>', lambda I: Module.AdjustOffset([0, 2])) # RenderEngine Event Listener does not work for keyboard strokes.
        WindowRendering.bind('<Down>', lambda I: Module.AdjustOffset([0, -2]))
        WindowRendering.bind('<Configure>', Module.ScreenRotationResize) # Handle Screen Rotation

    def ScreenRotationResize(Module, Arguments): # In Case of Screen Rotation Grid Will Adapt

        global OffSet
        if not (LimitScreenSize((750, 750, 2000, 1100)) and GetScreenScale() >= 1 and GetScreenScale() <= 1.5): Module.Exit()
        OffSet[0] = 0 if Module.StudioApplication.Dimension[0] > int(WindowSize()[0] // Module.Arguments[0]) else (WindowSize()[0] / 2 - 0.5 * Module.Arguments[0] * (Module.StudioApplication.Dimension[0] - 0.5)) # Adjust in case of Screen Rotation
        OffSet[1] = 0 if Module.StudioApplication.Dimension[1] > int(WindowSize()[1] // Math.sqrt(3 * Module.Arguments[0] ** 2 / 4)) else (WindowSize()[1] / 2 - 0.5 * Math.sqrt(3 * Module.Arguments[0] ** 2 / 4) * Module.StudioApplication.Dimension[1])       
            
    def AdjustOffset(Module, Input):

        global OffSet # Apply Offset adjustment, and check, if offsets take screen off canvas.
        if OffSet[0] + Input[0] <= 0 and WindowSize()[0] - OffSet[0] - Input[0] < Module.Arguments[0] * (Module.StudioApplication.Dimension[0]): OffSet[0] += Input[0]
        if OffSet[1] + Input[1] <= 0 and WindowSize()[1] - OffSet[1] - Input[1] < Module.StudioApplication.Dimension[1] * Math.sqrt(3 * (Module.Arguments[0]) ** 2 / 4): OffSet[1] += Input[1]
        Module.StudioApplication.RenderGrid()

    def UpdateGridMap(Module):

        Module.GridMap = list(ToolI(*[[XPosition for XPosition in YPosition]
        for YPosition in Module.StudioApplication.Grid])) # List out all the Grid Cell Modules

        Grid = []

        for _ in Module.GridMap: 
            
            if _ != None:
                
                if _.Data[2] is True: Grid.append((_.Index, _.Data[0], _.Data[1])) # Select only activated cells

        Module.GridMap = Grid

    def Import(Module, Name = None):

        if Name == None:

            with ToolII(FileNotFoundError):

                FileSource = FileOpen(filetypes=[("Bauxite Designs", "*.baux")]) # File Dialog (Import File)

        else:

            FileSource = Name

        if FileSource != "":

            FileSource = FileManage.load(open(FileSource, "r", encoding="utf-8")) # Load .baux file as readonly in 'utf-8'

            if FileSource["Grid Size"][0] >= 10 and FileSource["Grid Size"][1] >= 10 and FileSource["Grid Size"][0] <= 80 and FileSource["Grid Size"][1] <= 40:

                global OffSet
                OffSet[0] = 0 if FileSource["Grid Size"][0] > int(WindowSize()[0] // 50) else (WindowSize()[0] / 2 - 0.5 * 50 * (FileSource["Grid Size"][0] - 0.5))# Reset OffSet to [0, 0] if Screen Smaller than File Dimensions (0.5 is for Grid Offset of 1/2 Cell)
                OffSet[1] = 0 if FileSource["Grid Size"][1] > int(WindowSize()[1] // Math.sqrt(3 * 50 ** 2 / 4)) else (WindowSize()[1] / 2 - 0.5 * Math.sqrt(3 * 50 ** 2 / 4) * FileSource["Grid Size"][1]) # Otherwise, Align it in the center of the screen.
                Module.StudioApplication.RunProgram = False
                Module.StudioApplication = Grid(Module, 50, 
                Input = [(_[0], _[1], _[2]) for _ in FileSource["Data"]], # Load Existing Data Points
                Dimension = (FileSource["Grid Size"][0], FileSource["Grid Size"][1])) # Grid Size
                Module.UpdateGridMap()
                WindowRendering.after(25, Module.StudioApplication.RenderGrid) # Update Grid
                UpdateScreen()

            else: print(f"Error: {FileSource["Name"]}.baux does not meet the Grid Size Requirements (At least 10 by 10 cells / Smaller than 80 by 40 cells)\n")

    def Save(Module):

        FileSource = FileSaveI(filetypes=[("Bauxite Designs", "*.baux")], defaultextension=".baux")

        if FileSource != None:

            Module.UpdateGridMap()
        
            FileManage.dump(({
                "Name": System.path.splitext(System.path.basename(FileSource.name))[0],
                "Cell Size": Module.Arguments[0],
                "Grid Size": Module.StudioApplication.Dimension,
                "Data": Module.GridMap
            }), FileSource)

            Module.StudioApplication.RunProgram = False

            WindowRendering.destroy()

    def Export(Module):

        with ToolII(FileNotFoundError):

            FileSource = FileSaveII(filetypes=[("Scalable Vector Graphics", "*.svg")], defaultextension=".svg")

        if FileSource != "":

            Module.StudioApplication.ExportSVG.save_svg(FileSource)

    def Reset(Module):

        global OffSet
        OffSet = [0, 0]
        Module.StudioApplication.RunProgram = False # Removes Game Event Loop
        Module.StudioApplication = Grid(Module, Module.Arguments[0], Dimension = [0, 0])
        Module.UpdateGridMap() # Updates Values of Map of Selected Cells
        WindowRendering.after(25, Module.StudioApplication.RenderGrid)
    
    def Exit(Module):

        Module.GridMap = []
        Module.StudioApplication.RunProgram = False
        RenderEngine.display.quit() # End RenderEngine Process
        WindowRendering.destroy() # Close Application
        print("Session Completed.\n")

# --------- Command Line Interface ---------

class StudioTextElementI:
    
    def __init__(Module):

        ClearEntireConsole()

        print("\nBistable Auxetic Surface Studio:\n")

        if LimitScreenSize((750, 750, 2000, 1100)) and GetScreenScale() >= 1 and GetScreenScale() <= 1.5:

            print("Opening Editor:\n")

            Module.StageI = StudioGraphicalElementI([50,])

        elif GetScreenScale() < 1 or GetScreenScale() > 1.5:

            print("\nError: Screen Scale (DPI) must be between 100 - 150%.\n")
        
        else:

            print("\nError: Screen is too large or small.\n")

# --------- Main Interface ---------

Studio = StudioTextElementI()

# ----------------------------------

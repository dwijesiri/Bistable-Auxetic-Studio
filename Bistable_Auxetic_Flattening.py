# -------- Imports --------

import numpy as Data
import torch as Optimize
import trimesh as Mesh
import matplotlib.pyplot as Plot
from matplotlib import style as StyleI
import matplotx as StyleII
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import math as Math
import json as FileManage
import os as System
import mouette as MeshOperations
from time import time as Time

# -------- Utilities --------

Device = 'cuda' if Optimize.cuda.is_available() else 'cpu'

Resolutions = [10, 15, 20, 25, 30]

Sine = lambda I: Math.sin(Math.radians(I))

Cosine = lambda I: Math.cos(Math.radians(I))

Tangent = lambda I: Math.tan(Math.radians(I))

ClearScreen = lambda: System.system('clear' if System.name != 'nt' else 'cls')

ClearScreen()

print("\nBistable Auxetic Flattening Algorithm:")

print("\nPlease Select A Resolution (Defaults To #5): \n")

for _ in range(len(Resolutions)): print(f"{_ + 1} | ({Resolutions[_]} By {Resolutions[_]} Pixels) -> {int(Resolutions[_] * Math.sqrt(3)) * Resolutions[_]} Triangles")

Resolution = input("\nResolution: ")

Resolution = Resolution if Resolution.isdigit() else 5

Resolution = Resolution if 0 < int(Resolution) <= 5 else 5

print("\033[A\033[A") 
print("\033[A\033[A") 
print(f"\nResolution: #{Resolution}")

Resolution = Resolutions[int(Resolution) - 1]

# -------- Main Program --------

File = input("\nFile Path: ")

def Area(Points):

    VectorI = Data.array(Points[1]) - Data.array(Points[0])
    VectorII = Data.array(Points[2]) - Data.array(Points[0])
    Output = Data.cross(VectorI, VectorII)
    Output = Data.linalg.norm(Output)
    return Output

def ExpansionSize(Thickness, Theta, CellSize = 50, JointWidth = 1):

    ParameterI = (((CellSize - (1.5 * Thickness) - (Sine(60) * Thickness / Tangent(60 - Theta))) / (1 + (Tangent(Theta) / Tangent(60 - Theta)))) / Cosine(Theta)) - JointWidth # Length of Each Auxetic Line (2.5 is Gap Width)
    ParameterII = ((Sine(60) * Thickness) / Sine(60 - Theta)) + ((ParameterI + JointWidth) * Sine(Theta)) / Sine(60 - Theta)
    Expansion = 2 * (ParameterI - ParameterII) * Sine(Theta + 30)
    Expansion = 1 + (Expansion / CellSize)
    return Expansion

def LossComponent(Thickness, Theta, CellSize = 50, JointWidth = 1):

    ParameterI = Optimize.sin(Optimize.deg2rad(Optimize.tensor(60.0).to(Device))) # Sine (60)
    ParameterII = Optimize.sin(Optimize.deg2rad(Theta)) # Sine (Theta)
    ParameterIII = Optimize.cos(Optimize.deg2rad(Theta)) # Cosine (Theta)
    ParameterIV = Optimize.tan(Optimize.deg2rad(Theta)) # Tangent (Theta)
    ParameterV = Optimize.tan(Optimize.deg2rad(60.0 - Theta)) # Tangent (60 - Theta)
    ParameterVI = Optimize.sin(Optimize.deg2rad(60.0 - Theta)) # Sine (60 - Theta)
    ParameterVII = (((CellSize - (1.5 * Thickness) - (ParameterI * Thickness / ParameterV)) / (1 + (ParameterIV / ParameterV))) / ParameterIII) - JointWidth # Length of Each Auxetic Line (2.5 is Gap Width)
    ParameterVIII = ((ParameterI * Thickness) / ParameterVI) + ((ParameterVII + JointWidth) * ParameterII) / ParameterVI
    ParameterIX = Optimize.sin(Optimize.deg2rad(Theta + 30.0))
    Expansion = 2 * (ParameterVII - ParameterVIII) * ParameterIX
    Expansion = 1 + (Expansion / CellSize)
    return Expansion

# -------- Boundary First Flattening --------

print("\nBoundary First Flattening:\n")

MeshSource = MeshOperations.mesh.load(File)
Scale = MeshSource.vertices.create_attribute("scale_factor", float)
Scale[MeshSource.boundary_vertices[0]] = 0
Scale[MeshSource.boundary_vertices[4]] = 0
BoundaryFirstFlattening = MeshOperations.parametrization.BoundaryFirstFlattening(MeshSource, bnd_scale_fctr = Scale, verbose = True)
MeshSource = BoundaryFirstFlattening.run()
MeshOperations.mesh.save(MeshSource, "Initial.obj")
MeshOperations.mesh.save(BoundaryFirstFlattening.flat_mesh, "Target.obj")

# -------- Get Expansion And Scaling --------

Target = Mesh.load("Target.obj")
TargetFaces = Target.faces
TargetVertices = Target.vertices
TargetAreas = Data.array([Area(TargetVertices[Face]) for Face in TargetFaces])

Initial = Mesh.load("Initial.obj")
InitialFaces = Initial.faces
InitialVertices = Initial.vertices
InitialAreas = Data.array([Area(InitialVertices[Face]) for Face in InitialFaces])

ExpansionFactors = Data.sqrt(InitialAreas / TargetAreas)

if min(ExpansionFactors) < 1: ExpansionFactors += (1 - min(ExpansionFactors))

# -------- Visualisation --------

print("\nDistribution of Expansion:\n")

Plot.rcParams["font.family"] = "Bell MT"
StyleI.use(StyleII.styles.dracula)
Plot.box(False)
Plot.title("Expansion Factors")
Plot.plot(ExpansionFactors, linewidth = 0.5)
Plot.show()

print("3D Expansion Heatmap:\n")

StyleI.use('default')
Plot.rcParams["font.family"] = ["Bell MT", "sans-serif"]
Figure = Plot.figure()
Graph = Plot.axes()
Faces = Target.triangles_center
Shifting = [-min(Target.triangles_center[:, _]) for _ in range(3)]
#ExpansionFactors = 1.1 + ((ExpansionFactors - min(ExpansionFactors)) * 0.85 / (max(ExpansionFactors) - min(ExpansionFactors)))
Faces = Faces + Shifting
Scaling = min([Resolution / max(Faces[:, _]) for _ in range(2)])
Faces = Faces * Scaling
Values = Graph.tripcolor(*(Target.vertices[:, 0], Target.vertices[:, 1]), Target.faces, ExpansionFactors, alpha = 0.55, lw = 0)
Graph.set_aspect('equal')
Figure.colorbar(ScalarMappable(cmap = 'viridis', norm = Normalize(vmin = min(ExpansionFactors), vmax = max(ExpansionFactors))), ax = Graph)
Plot.box(False)
Plot.show()
Faces = Faces * [Math.sqrt(3), 1, 1]
StartTime = Time()

# -------- Optimize For .Baux File --------

Expansion = Data.zeros((int((Resolution + 1) * Math.sqrt(3)), int(Resolution + 1), 2))

for _ in range(len(ExpansionFactors)): 
    
    Expansion[int(Faces[_][0]), int(Faces[_][1]), 1] += ExpansionFactors[_]
    Expansion[int(Faces[_][0]), int(Faces[_][1]), 0] += 1

print("Checking For Matching Points:\n")

def Optimized(TargetExpansion, LearningRate = 5e-2, Iterations = 1150, BatchSize = 64):

    Thickness = Optimize.full((BatchSize,), 2.5, requires_grad = True, device = Device)
    Theta = Optimize.full((BatchSize,), 5.5, requires_grad = True, device = Device)
    Optimizer = Optimize.optim.Adam([Thickness, Theta], lr = LearningRate)
    TargetValue = Optimize.tensor(TargetExpansion, dtype = Optimize.float32, device = Device)

    for _ in range(Iterations):

        Optimizer.zero_grad()
        ExpansionBatch = LossComponent(Thickness, Theta)
        Loss = Optimize.nn.functional.mse_loss(ExpansionBatch, TargetValue)
        Loss.backward()
        Optimizer.step()
        Thickness.data.clamp_(1.5, 13.5)
        Theta.data.clamp_(-5, 22.5)
        if float(Optimize.max(Optimize.abs(ExpansionBatch - TargetValue))) <= 1e-3: break
    
    return Thickness.detach().cpu().numpy(), Theta.detach().cpu().numpy()

CellList = [(X, Y, Expansion[X, Y, 1] / Expansion[X, Y, 0]) for X in range(int(Resolution * Math.sqrt(3))) for Y in range(Resolution) if Expansion[X, Y, 0] != 0]
BatchSize = 256
Batches = [CellList[Index: Index + BatchSize] for Index in range(0, len(CellList), BatchSize)]
DataExport = []
Index = 0
Error = 0

CellLength = Data.count_nonzero(Expansion[:, :, 0] != 0)

for Batch in Batches:

    XBatch, YBatch, ExpansionBatch = zip(*Batch)
    ExpansionBatch = Data.array(ExpansionBatch, dtype = Data.float32)
    ThicknessBatch, ThetaBatch = Optimized(ExpansionBatch, BatchSize = len(ExpansionBatch))

    for _ in range(len(Batch)):

        Index += 1
        X, Y, Thickness, Theta = XBatch[_], YBatch[_], ThicknessBatch[_], ThetaBatch[_]
        Loss = float(ExpansionSize(Thickness, Theta) - ExpansionBatch[_])
        if abs(Loss) >= 1e-3: Error += 1
        print(f"Index: {Index} / {CellLength}, Grid Cell: ({X}, {Y}), Expansion: {ExpansionBatch[_]:.3f}, Loss: {Loss:.3f}")
        DataExport.append([[int(X + 1), int(Y + 1)], float(round(Thickness, 3)), float(round(Theta, 3))])

EndTime = Time()

Error = (Error / CellLength) * 100

print(f"\nError Percentage {Error:.5f}%")

print(f"\nTotal Time: {(EndTime - StartTime):.5f} Seconds")

# -------- Saving Data To File --------

FileName = input("\nFile Name: ")

print("\033[A\033[A") 

print(f"File Name: {FileName}.baux\n")

FileManage.dump(({
    "Name": FileName, 
    "Cell Size": 50, 
    "Grid Size": [int(Resolution * Math.sqrt(3)), Resolution], 
    "Data": DataExport,
}), open(f"{FileName}.baux", "w"))
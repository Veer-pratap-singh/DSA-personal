import streamlit as st
import json
import os
import pandas as pd
from datetime import date

# Set page configuration for layout and styling
st.set_page_config(
    page_title="GATE Data Science & AI (DA) Study Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. GATE DA Curriculum Database (180 Days)
# ==========================================
STUDY_PLAN = [
    {
        "week": 1,
        "name": "Matrices & Systems of Linear Equations",
        "phase": "phase1",
        "subject": "Linear Algebra",
        "days": [
            { "id": 1, "title": "Vector Operations & Combinations", "focus": "Vectors, scalar multiplication, linear combinations, span", "resource": "GO Classes Linear Algebra - Lec 1-3", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
            { "id": 2, "title": "Linear Independence & Dependence", "focus": "Linearly independent vector sets, verifying dependencies", "resource": "3Blue1Brown Linear Algebra - Lec 2", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab" },
            { "id": 3, "title": "Systems of Linear Equations (Ax = b)", "focus": "Matrix representations, coefficients, augmentations", "resource": "GO Classes Linear Algebra - Lec 4-6", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
            { "id": 4, "title": "Gaussian Elimination & Row Echelon", "focus": "Row operations, pivots, row echelon vs reduced row echelon", "resource": "GO Classes Linear Algebra - Lec 7-9", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
            { "id": 5, "title": "Rank of a Matrix", "focus": "Pivot variables, rank definition, rank calculation", "resource": "GO Classes Linear Algebra - Lec 10-12", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
            { "id": 6, "title": "Nullity & Rank-Nullity Theorem", "focus": "Free variables, null space, rank-nullity formulation", "resource": "GO Classes Linear Algebra - Lec 13-15", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
            { "id": 7, "title": "Weekly Review & Practice", "focus": "Practice solving system of equations, write cheat sheet", "resource": "GO Classes Linear Algebra Playlist", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" }
        ]
    },
    {
        "week": 2,
        "name": "Vector Spaces & Fundamental Subspaces",
        "phase": "phase1",
        "subject": "Linear Algebra",
        "days": [
            { "id": 8, "title": "Vector Spaces & Subspaces", "focus": "Definition axioms, subspace requirements, span subspaces", "resource": "GO Classes Linear Algebra - Lec 16-18", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
            { "id": 9, "title": "Subspace Intersection & Sum", "focus": "Verifying if intersections or unions form subspaces", "resource": "Gilbert Strang Linear Algebra Notes", "url": "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/4d876a9159e32543eb0d73b4d4382f4c_MIT18_06S10ZoomNotes.pdf" },
            { "id": 10, "title": "Bases & Dimension", "focus": "Definition of basis, uniqueness, computing dimensions", "resource": "GO Classes Linear Algebra - Lec 19-21", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
            { "id": 11, "title": "Change of Basis Matrix", "focus": "Transformation matrix from basis B1 to B2", "resource": "3Blue1Brown Linear Algebra - Lec 13", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab" },
            { "id": 12, "title": "The Four Fundamental Subspaces", "focus": "Definitions of C(A), N(A), C(A^T), N(A^T)", "resource": "GO Classes Linear Algebra - Lec 22-24", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
            { "id": 13, "title": "Subspace Dimensions & Relations", "focus": "Finding dimensions of the 4 subspaces for mxn matrix", "resource": "GO Classes Linear Algebra - Lec 25-27", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
            { "id": 14, "title": "Bases & Subspaces Practice", "focus": "Solve past GATE questions on vectors & subspaces", "resource": "GATE Overflow Linear Algebra Questions", "url": "https://gateoverflow.in/tag/linear-algebra" }
        ]
    },
    {
        "week": 3,
        "name": "Determinants, Transformations & Eigenvalues",
        "phase": "phase1",
        "subject": "Linear Algebra",
        "days": [
            { "id": 15, "title": "Matrix Multiplication & Inverse", "focus": "Properties, computational tricks, Gauss-Jordan inverse", "resource": "3Blue1Brown Linear Algebra - Lec 4", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab" },
            { "id": 16, "title": "Linear Transformations & Kernel", "focus": "Linearity checks, image and kernel definitions", "resource": "3Blue1Brown Linear Algebra - Lec 3", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab" },
            { "id": 17, "title": "Determinants & Properties", "focus": "Determinant calculation, row ops effects, volume expansion", "resource": "GO Classes Linear Algebra - Lec 28-30", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
            { "id": 18, "title": "Cramer's Rule & Formula", "focus": "Solving systems via Cramer's rule, cofactor formula", "resource": "GO Classes Linear Algebra - Lec 31-33", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
            { "id": 19, "title": "Eigenvalues & Eigenvectors", "focus": "Characteristic equation, solving det(A - λI) = 0", "resource": "GO Classes Linear Algebra - Lec 34-36", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
            { "id": 20, "title": "Diagonalization & Similarity", "focus": "Symmetric matrices, algebraic vs geometric multiplicity", "resource": "GO Classes Linear Algebra - Lec 37-39", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
            { "id": 21, "title": "Transformation & Eigenvalue practice", "focus": "Practice solving eigenvalues from GATE CS/EC papers", "resource": "GATE Overflow Linear Algebra Questions", "url": "https://gateoverflow.in/tag/linear-algebra" }
        ]
    },
    {
        "week": 4,
        "name": "Orthogonality & Matrix Decompositions",
        "phase": "phase1",
        "subject": "Linear Algebra",
        "days": [
            { "id": 22, "title": "Inner Product & Orthogonality", "focus": "Dot products, lengths, angles, orthogonal vector spaces", "resource": "GO Classes Linear Algebra - Lec 40-42", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
            { "id": 23, "title": "Orthogonal Projections", "focus": "Projection onto lines, projection matrices", "resource": "GO Classes Linear Algebra - Lec 43-45", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
            { "id": 24, "title": "Gram-Schmidt & QR Decomposition", "focus": "Orthonormal basis construction, A = QR breakdown", "resource": "GO Classes Linear Algebra - Lec 46-48", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
            { "id": 25, "title": "LU Decomposition", "focus": "Lower-Upper matrix decomposition, forwards-back substitution", "resource": "GO Classes Linear Algebra - Lec 49-51", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
            { "id": 26, "title": "Singular Value Decomposition (SVD)", "focus": "Mathematical formula, singular values, U Σ V^T properties", "resource": "GO Classes Linear Algebra - Lec 52-54", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
            { "id": 27, "title": "Matrix Decomposition Problems", "focus": "Practice LU, QR, and SVD calculation", "resource": "Maths for ML Deisenroth Textbook", "url": "https://mml-book.github.io/book/mml-book.pdf" },
            { "id": 28, "title": "Linear Algebra Subject Test", "focus": "Solve 30-question subject test. Analyze error log", "resource": "GATE Overflow Linear Algebra Questions", "url": "https://gateoverflow.in/tag/linear-algebra" }
        ]
    },
    {
        "week": 5,
        "name": "Probability Basics & Bayes' Theorem",
        "phase": "phase1",
        "subject": "Probability & Statistics",
        "days": [
            { "id": 29, "title": "Sample Space, Events & Axioms", "focus": "Basic probability rules, Venn diagrams, set operations", "resource": "GO Classes Probability - Lec 1-3", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" },
            { "id": 30, "title": "Permutations & Combinations in Prob.", "focus": "Counting principles, balls & bins, combinations selection", "resource": "Probability Course - Combinatorics", "url": "https://www.probabilitycourse.com/chapter1/1_3_0_combinatorics.php" },
            { "id": 31, "title": "Conditional Probability & Independence", "focus": "Multiplication rule, independent events definition", "resource": "GO Classes Probability - Lec 4-6", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" },
            { "id": 32, "title": "Total Probability Theorem", "focus": "Partitioning sample space, weighted probabilities sum", "resource": "GO Classes Probability - Lec 4-6", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" },
            { "id": 33, "title": "Bayes' Theorem", "focus": "Posterior probability calculation, base rate fallacy", "resource": "3Blue1Brown Bayes Theorem Video", "url": "https://www.youtube.com/watch?v=HZGCoVF3YvM" },
            { "id": 34, "title": "Bayes' Theorem Advanced Scenarios", "focus": "Multiple observations, conditional independence in Bayes", "resource": "GO Classes Probability Playlist", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" },
            { "id": 35, "title": "Bayes' & Probability Practice", "focus": "Solve 20 problems on conditional probability", "resource": "GATE Overflow Probability Questions", "url": "https://gateoverflow.in/tag/probability" }
        ]
    },
    {
        "week": 6,
        "name": "Random Variables & Distributions",
        "phase": "phase1",
        "subject": "Probability & Statistics",
        "days": [
            { "id": 36, "title": "Discrete Random Variables (PMF, CDF)", "focus": "Probability mass function, cumulative steps, mean, variance", "resource": "GO Classes Probability - Lec 7-9", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" },
            { "id": 37, "title": "Expectation & Variance Properties", "focus": "Linearity of expectation, scaling variance, moments", "resource": "Probability Course - Expectation & Variance", "url": "https://www.probabilitycourse.com/chapter3/3_1_2_expectation_variance.php" },
            { "id": 38, "title": "Continuous Random Variables (PDF, CDF)", "focus": "Integration of density, cumulative distributions, mean, variance", "resource": "GO Classes Probability - Lec 10-12", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" },
            { "id": 39, "title": "Binomial & Poisson Distributions", "focus": "Derivations, PMFs, mean, variance, Poisson approximation", "resource": "GO Classes Probability - Lec 13-15", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" },
            { "id": 40, "title": "Uniform, Exponential & Geometric Dist.", "focus": "Memoryless property of exponential & geometric, integrations", "resource": "GO Classes Probability - Lec 16-18", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" },
            { "id": 41, "title": "Normal (Gaussian) Distribution", "focus": "PDF, standard normal conversion, Z-table usage, properties", "resource": "GO Classes Probability - Lec 19-21", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" },
            { "id": 42, "title": "Distribution Summary & Short Notes", "focus": "Write formula sheet for all distributions, solve 15 questions", "resource": "GO Classes Probability Playlist", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" }
        ]
    },
    {
        "week": 7,
        "name": "Joint Distributions & Limit Theorems",
        "phase": "phase1",
        "subject": "Probability & Statistics",
        "days": [
            { "id": 43, "title": "Joint PMF & PDF", "focus": "Marginals, joint CDF, integration limits, double integration", "resource": "GO Classes Probability - Lec 22-24", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" },
            { "id": 44, "title": "Conditional Distributions & Independence", "focus": "Independent random variables, conditional density", "resource": "Probability Course - Conditional Distributions", "url": "https://www.probabilitycourse.com/chapter5/5_1_3_conditional_distributions.php" },
            { "id": 45, "title": "Covariance & Correlation", "focus": "Mathematical formula, properties, correlation coefficient", "resource": "GO Classes Probability - Lec 25-27", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" },
            { "id": 46, "title": "Sum of Independent Random Variables", "focus": "Convolutions of discrete and continuous variables", "resource": "GO Classes Probability - Lec 28-30", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" },
            { "id": 47, "title": "Chebyshev's Inequality", "focus": "Bounding probability using mean and variance", "resource": "GO Classes Probability - Lec 31-33", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" },
            { "id": 48, "title": "LLN & Central Limit Theorem", "focus": "Law of Large Numbers, CLT application to approximations", "resource": "GO Classes Probability - Lec 34-36", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" },
            { "id": 49, "title": "Joint Distributions & Limits Practice", "focus": "Solve past GATE questions on CLT & Covariance", "resource": "GATE Overflow Probability Questions", "url": "https://gateoverflow.in/tag/probability" }
        ]
    },
    {
        "week": 8,
        "name": "Statistical Inference",
        "phase": "phase1",
        "subject": "Probability & Statistics",
        "days": [
            { "id": 50, "title": "Sampling Distributions", "focus": "Sample mean, sample variance, Chi-square & Student-t", "resource": "Wasserman All of Statistics PDF", "url": "https://egrcc.github.io/docs/math/all-of-statistics.pdf" },
            { "id": 51, "title": "Point Estimation & Bias", "focus": "Estimator definition, unbiasedness, Mean Squared Error", "resource": "NPTEL Statistical Inference", "url": "https://nptel.ac.in/courses/111105039" },
            { "id": 52, "title": "Maximum Likelihood Estimation (MLE)", "focus": "Likelihood functions, log-likelihood optimization, MLE steps", "resource": "GO Classes Probability Playlist", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" },
            { "id": 53, "title": "Hypothesis Testing Basics", "focus": "Null/Alternative, Type I & II errors, significance level", "resource": "NPTEL Hypothesis Testing", "url": "https://nptel.ac.in/courses/111105039" },
            { "id": 54, "title": "z-test & t-test Procedures", "focus": "One-sample, two-sample tests, critical values, p-value", "resource": "Wasserman All of Statistics PDF", "url": "https://egrcc.github.io/docs/math/all-of-statistics.pdf" },
            { "id": 55, "title": "Chi-Square Test & Likelihood Ratio", "focus": "Goodness of fit, independence tests", "resource": "NPTEL Statistical Inference - Lec 30", "url": "https://nptel.ac.in/courses/111105039" },
            { "id": 56, "title": "Probability & Stats Subject Test", "focus": "Practice full Statistics subject test, log mistakes", "resource": "GATE Overflow Probability Questions", "url": "https://gateoverflow.in/tag/probability" }
        ]
    },
    {
        "week": 9,
        "name": "Single-Variable Calculus",
        "phase": "phase1",
        "subject": "Calculus & Optimization",
        "days": [
            { "id": 57, "title": "Limits & Continuity", "focus": "L'Hopital's rule, continuity conditions, limits evaluations", "resource": "3Blue1Brown Calculus - Lec 1-3", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr" },
            { "id": 58, "title": "Differentiability of Functions", "focus": "Checking differentiability, left/right hand derivatives", "resource": "GeeksforGeeks Calculus Study Guide", "url": "https://www.geeksforgeeks.org/calculus-for-gate-syllabus/" },
            { "id": 59, "title": "Mean Value Theorems", "focus": "Rolle's Theorem, Lagrange MVT, Cauchy MVT applications", "resource": "GeeksforGeeks Calculus Study Guide", "url": "https://www.geeksforgeeks.org/calculus-for-gate-syllabus/" },
            { "id": 60, "title": "Taylor & Maclaurin Series", "focus": "Power series expansion, approximations, error term", "resource": "3Blue1Brown Calculus - Lec 11", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr" },
            { "id": 61, "title": "Single Variable Maxima & Minima", "focus": "First & second derivative tests, critical points", "resource": "GeeksforGeeks Calculus Study Guide", "url": "https://www.geeksforgeeks.org/calculus-for-gate-syllabus/" },
            { "id": 62, "title": "Integration Basics & FTC", "focus": "Fundamental Theorem of Calculus, standard integrals", "resource": "3Blue1Brown Calculus - Lec 8", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr" },
            { "id": 63, "title": "Single-Variable Calculus Practice", "focus": "Solve 20 calculus questions from past GATE papers", "resource": "GATE Overflow Calculus Questions", "url": "https://gateoverflow.in/tag/calculus" }
        ]
    },
    {
        "week": 10,
        "name": "Multivariable Calculus & Optimization",
        "phase": "phase1",
        "subject": "Calculus & Optimization",
        "days": [
            { "id": 64, "title": "Partial Derivatives & Chain Rule", "focus": "Multivariable differentiation, total derivatives", "resource": "GeeksforGeeks Calculus Study Guide", "url": "https://www.geeksforgeeks.org/calculus-for-gate-syllabus/" },
            { "id": 65, "title": "Gradient Vector & Directional Deriv.", "focus": "Computing gradient vector, geometrical interpretation", "resource": "3Blue1Brown Calculus - Lec 13", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr" },
            { "id": 66, "title": "Hessian Matrix & Taylor Exp", "focus": "Hessian calculation, quadratic form approximations", "resource": "Maths for ML Deisenroth Textbook", "url": "https://mml-book.github.io/book/mml-book.pdf" },
            { "id": 67, "title": "Multivariable Maxima & Minima", "focus": "Saddle points, critical points checks using Hessian", "resource": "GeeksforGeeks Calculus Study Guide", "url": "https://www.geeksforgeeks.org/calculus-for-gate-syllabus/" },
            { "id": 68, "title": "Unconstrained Optimization Basics", "focus": "Objective function, local vs global minima definition", "resource": "NPTEL Optimization Methods", "url": "https://nptel.ac.in/courses/111105039" },
            { "id": 69, "title": "Gradient Descent Algorithm", "focus": "Learning rate, updates, divergence, convergence criteria", "resource": "Maths for ML Deisenroth Textbook", "url": "https://mml-book.github.io/book/mml-book.pdf" },
            { "id": 70, "title": "Calculus & Optimization Subject Test", "focus": "Complete optimization subject test, log mistakes", "resource": "GATE Overflow Calculus Questions", "url": "https://gateoverflow.in/tag/calculus" }
        ]
    },
    {
        "week": 11,
        "name": "Python Basics & Complexity",
        "phase": "phase2",
        "subject": "Programming & DSA",
        "days": [
            { "id": 71, "title": "Python Syntax & Basic Types", "focus": "Variables, print formatting, arithmetic operations", "resource": "NPTEL Programming in Python - Week 1", "url": "https://nptel.ac.in/courses/106106145" },
            { "id": 72, "title": "Python Data Structures", "focus": "Lists, tuples, dictionaries, sets, control flow loops", "resource": "NPTEL Programming in Python - Week 2", "url": "https://nptel.ac.in/courses/106106145" },
            { "id": 73, "title": "Functions & Lambda Expressions", "focus": "Parameter passing, scopes, inline anonymous lambdas", "resource": "NPTEL Programming in Python - Week 3", "url": "https://nptel.ac.in/courses/106106145" },
            { "id": 74, "title": "Complexity Analysis Notations", "focus": "Big-O, Omega, Theta, asymptotic math analysis", "resource": "GeeksforGeeks Complexity Guide", "url": "https://www.geeksforgeeks.org/fundamentals-of-algorithms/" },
            { "id": 75, "title": "Recursion & Recurrence Relations", "focus": "Solving recurrences, substitution, Master's Theorem", "resource": "Madhavan Mukund DSA Python - Week 4", "url": "https://nptel.ac.in/courses/106106145" },
            { "id": 76, "title": "Arrays & Linked Lists (Python)", "focus": "Singly, doubly linked list ops, complexity comparison", "resource": "GeeksforGeeks Python DSA Guide", "url": "https://www.geeksforgeeks.org/python-data-structures-and-algorithms/" },
            { "id": 77, "title": "Python & Complexity Exercises", "focus": "Code snippet dry runs, find time complexity of codes", "resource": "GATE Overflow Complexity Questions", "url": "https://gateoverflow.in/tag/complexity" }
        ]
    },
    {
        "week": 12,
        "name": "Trees, Graphs, Sorting & Searching",
        "phase": "phase2",
        "subject": "Programming & DSA",
        "days": [
            { "id": 78, "title": "Stacks & Queues", "focus": "Implementation using list/deque, applications (DFS/BFS)", "resource": "GeeksforGeeks Python DSA Guide", "url": "https://www.geeksforgeeks.org/python-data-structures-and-algorithms/" },
            { "id": 79, "title": "Binary Trees & Traversals", "focus": "Inorder, preorder, postorder traversals, reconstruction", "resource": "Madhavan Mukund DSA Python - Week 5", "url": "https://nptel.ac.in/courses/106106145" },
            { "id": 80, "title": "Binary Search Trees (BST) & Heaps", "focus": "Search property, insertion, min/max heap heapify ops", "resource": "Madhavan Mukund DSA Python - Week 6", "url": "https://nptel.ac.in/courses/106106145" },
            { "id": 81, "title": "Sorting Algorithms (Merge, Quick)", "focus": "Divide & conquer, pivot selections, average vs worst cases", "resource": "Madhavan Mukund DSA Python - Week 2", "url": "https://nptel.ac.in/courses/106106145" },
            { "id": 82, "title": "Heapsort, Bubble, Insert, Select", "focus": "Time/space complexities, stability of sorts", "resource": "Madhavan Mukund DSA Python - Week 3", "url": "https://nptel.ac.in/courses/106106145" },
            { "id": 83, "title": "Graphs Traversals (BFS & DFS)", "focus": "Adjacency matrix/list representation, BFS, DFS code", "resource": "Madhavan Mukund DSA Python - Week 7", "url": "https://nptel.ac.in/courses/106106145" },
            { "id": 84, "title": "DSA Subject Mock Test", "focus": "Take 30-question DSA quiz, record mistakes", "resource": "GATE Overflow DSA Questions", "url": "https://gateoverflow.in/tag/data-structures" }
        ]
    },
    {
        "week": 13,
        "name": "ER Model & Relational Algebra",
        "phase": "phase2",
        "subject": "DBMS & Warehousing",
        "days": [
            { "id": 85, "title": "Entity-Relationship (ER) Model", "focus": "Entities, attributes, primary key, relationships, mapping", "resource": "Amit Khurana DBMS Playlist", "url": "https://tinyurl.com/AK-DBMS-GATE" },
            { "id": 86, "title": "Relational Model Concepts", "focus": "Schema, relations, constraints (domain, referential integrity)", "resource": "NPTEL Database Design - Lec 5", "url": "https://nptel.ac.in/courses/106105175" },
            { "id": 87, "title": "Keys (Super, Candidate, Primary, Foreign)", "focus": "Identifying candidate keys from functional dependencies", "resource": "Amit Khurana DBMS Playlist", "url": "https://tinyurl.com/AK-DBMS-GATE" },
            { "id": 88, "title": "Relational Algebra Operations", "focus": "Selection, Projection, Join (Natural, Theta, Outer), Union", "resource": "NPTEL Relational Algebra", "url": "https://nptel.ac.in/courses/106105175" },
            { "id": 89, "title": "SQL Basics (SELECT, WHERE, GROUP BY)", "focus": "Query syntax, aggregates, having clause, filtering", "resource": "Amit Khurana DBMS Playlist", "url": "https://tinyurl.com/AK-DBMS-GATE" },
            { "id": 90, "title": "Advanced SQL (Joins & Subqueries)", "focus": "Nested queries, correlated subqueries, left/right outer joins", "resource": "NPTEL SQL Lectures", "url": "https://nptel.ac.in/courses/106105175" },
            { "id": 91, "title": "Relational Algebra & SQL Practice", "focus": "Solve 20 SQL/RA query translation problems", "resource": "GATE Overflow DBMS Questions", "url": "https://gateoverflow.in/tag/dbms" }
        ]
    },
    {
        "week": 14,
        "name": "Normalization, Transactions & Warehousing",
        "phase": "phase2",
        "subject": "DBMS & Warehousing",
        "days": [
            { "id": 92, "title": "Functional Dependencies", "focus": "FD rules, attribute closure, equivalence of FD sets", "resource": "Amit Khurana DBMS Playlist", "url": "https://tinyurl.com/AK-DBMS-GATE" },
            { "id": 93, "title": "Normal Forms (1NF, 2NF, 3NF, BCNF)", "focus": "Lossless joins, dependency preservation, normal form check", "resource": "NPTEL Normalization Lectures", "url": "https://nptel.ac.in/courses/106105175" },
            { "id": 94, "title": "Transaction ACID Properties", "focus": "Atomicity, consistency, isolation, durability definitions", "resource": "Amit Khurana DBMS Playlist", "url": "https://tinyurl.com/AK-DBMS-GATE" },
            { "id": 95, "title": "Serializability & Concurrency Control", "focus": "Conflict serializable check (precedence graph), view serializability", "resource": "NPTEL Concurrency Control", "url": "https://nptel.ac.in/courses/106105175" },
            { "id": 96, "title": "File Organization & B+ Trees", "focus": "Indexing concepts, B/B+ tree insertions & capacities", "resource": "Amit Khurana DBMS Playlist", "url": "https://tinyurl.com/AK-DBMS-GATE" },
            { "id": 97, "title": "Data Warehousing Basics", "focus": "Star schema, snowflake schema, OLAP operations (Rollup, Drilldown)", "resource": "GeeksforGeeks DBMS & Warehousing Guide", "url": "https://www.geeksforgeeks.org/data-warehousing-and-data-mining-tutorial/" },
            { "id": 98, "title": "DBMS & DW Subject Test", "focus": "Solve 35 DBMS questions, check normalization & SQL solutions", "resource": "GATE Overflow DBMS Questions", "url": "https://gateoverflow.in/tag/dbms" }
        ]
    },
    {
        "week": 15,
        "name": "ML Basics & Regression Models",
        "phase": "phase3",
        "subject": "Machine Learning",
        "days": [
            { "id": 99, "title": "Introduction to Machine Learning", "focus": "Types of learning, generalization, under/overfitting", "resource": "Stanford CS229 ML - Lecture 1", "url": "https://www.youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU" },
            { "id": 100, "title": "Bias-Variance Tradeoff", "focus": "Mathematical breakdown of MSE = Bias^2 + Var + Noise", "resource": "NPTEL Intro to ML - Lec 4", "url": "https://nptel.ac.in/courses/106106139" },
            { "id": 101, "title": "Simple Linear Regression", "focus": "OLS cost function, derivations of beta coefficients", "resource": "Stanford CS229 ML - Lecture 2", "url": "https://www.youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU" },
            { "id": 102, "title": "Multiple Linear Regression & OLS", "focus": "Matrix formula β = (X^T X)^-1 X^T y derivation", "resource": "Maths for ML Deisenroth Textbook", "url": "https://mml-book.github.io/book/mml-book.pdf" },
            { "id": 103, "title": "Regularization (Lasso, Ridge)", "focus": "L1 and L2 penalties, geometrical explanation of sparsity", "resource": "NPTEL Intro to ML - Lec 8", "url": "https://nptel.ac.in/courses/106106139" },
            { "id": 104, "title": "Cross-Validation & Grid Search", "focus": "K-fold, stratified K-fold, hyperparameter tuning", "resource": "Stanford CS229 ML - Lecture 5", "url": "https://www.youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU" },
            { "id": 105, "title": "Regression Practice Problems", "focus": "Compute gradient equations, regularized cost minimization", "resource": "Bishop Pattern Recognition Textbook (Microsoft PDF)", "url": "https://www.microsoft.com/en-us/research/uploads/prod/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf" }
        ]
    },
    {
        "week": 16,
        "name": "Classification Models & Decision Trees",
        "phase": "phase3",
        "subject": "Machine Learning",
        "days": [
            { "id": 106, "title": "Logistic Regression", "focus": "Sigmoid function, logistic loss function (cross-entropy)", "resource": "Stanford CS229 ML - Lecture 4", "url": "https://www.youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU" },
            { "id": 107, "title": "Logistic Regression Decision Boundary", "focus": "Linear decision boundaries, multi-class softmax", "resource": "NPTEL Intro to ML - Lec 12", "url": "https://nptel.ac.in/courses/106106139" },
            { "id": 108, "title": "Support Vector Machines (Hard Margin)", "focus": "Maximizing the margin, constraint optimization formulation", "resource": "NPTEL Intro to ML - Lec 18", "url": "https://nptel.ac.in/courses/106106139" },
            { "id": 109, "title": "SVM Soft Margin & Kernel Trick", "focus": "Slack variables, dual form, RBF/polynomial kernels", "resource": "Stanford CS229 ML - Lecture 6", "url": "https://www.youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU" },
            { "id": 110, "title": "Decision Trees Splitting Criteria", "focus": "Entropy, Gini impurity, Information Gain calculations", "resource": "NPTEL Intro to ML - Lec 15", "url": "https://nptel.ac.in/courses/106106139" },
            { "id": 111, "title": "Decision Tree Regressors & Pruning", "focus": "Variance reduction split, cost complexity pruning", "resource": "Maths for ML Deisenroth Textbook", "url": "https://mml-book.github.io/book/mml-book.pdf" },
            { "id": 112, "title": "Classification Models Practice", "focus": "Calculate entropy splits, trace SVM decision boundaries", "resource": "GATE Overflow ML Questions", "url": "https://gateoverflow.in/tag/machine-learning" }
        ]
    },
    {
        "week": 17,
        "name": "Naive Bayes, KNN & Neural Networks",
        "phase": "phase3",
        "subject": "Machine Learning",
        "days": [
            { "id": 113, "title": "Naive Bayes Classifier", "focus": "Bayes class rule, conditional independence, Laplace smoothing", "resource": "NPTEL Intro to ML - Lec 10", "url": "https://nptel.ac.in/courses/106106139" },
            { "id": 114, "title": "K-Nearest Neighbors (KNN)", "focus": "Distance metrics, boundary complexity based on k", "resource": "NPTEL Intro to ML - Lec 11", "url": "https://nptel.ac.in/courses/106106139" },
            { "id": 115, "title": "Multilayer Perceptron Structure", "focus": "Nodes, hidden layers, weights, bias, feedforward flow", "resource": "3Blue1Brown Neural Networks - Lec 1", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000DX_ZCJB-3Ky" },
            { "id": 116, "title": "Activation Functions", "focus": "Sigmoid, Tanh, ReLU, Leaky ReLU, Softmax and derivatives", "resource": "3Blue1Brown Neural Networks - Lec 2", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000DX_ZCJB-3Ky" },
            { "id": 117, "title": "Backpropagation Algorithm", "focus": "Chain rule for gradients, weights updates formulations", "resource": "3Blue1Brown Neural Networks - Lec 3-4", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000DX_ZCJB-3Ky" },
            { "id": 118, "title": "Neural Networks Practice", "focus": "Perform forward/backprop calculations on mini-network", "resource": "GO Classes NN Tutorials", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" },
            { "id": 119, "title": "Evaluation Metrics (ROC, AUC, F1)", "focus": "Precision, recall, confusion matrix, ROC-AUC plot", "resource": "Stanford CS229 ML - Lecture 11", "url": "https://www.youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU" }
        ]
    },
    {
        "week": 18,
        "name": "Unsupervised Learning & PCA",
        "phase": "phase3",
        "subject": "Machine Learning",
        "days": [
            { "id": 120, "title": "K-Means Clustering", "focus": "K-means Lloyd's algorithm, objective function, initialization", "resource": "Stanford CS229 ML - Lecture 12", "url": "https://www.youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU" },
            { "id": 121, "title": "K-Means Evaluation & Medoids", "focus": "Elbow method, silhouette score, k-medoids algorithm", "resource": "GFG K-Medoids Clustering Guide", "url": "https://www.geeksforgeeks.org/k-medoids-clustering-clustering-algorithms-in-machine-learning/" },
            { "id": 122, "title": "Hierarchical Clustering", "focus": "Agglomerative vs divisive, single, complete, average linkage", "resource": "GFG Hierarchical Clustering Guide", "url": "https://www.geeksforgeeks.org/hierarchical-clustering-in-data-mining/" },
            { "id": 123, "title": "PCA Concepts", "focus": "Dimensionality reduction, projection, variance maximization", "resource": "GFG Principal Component Analysis Guide", "url": "https://www.geeksforgeeks.org/principal-component-analysis-pca/" },
            { "id": 124, "title": "PCA Mathematical Derivation", "focus": "Covariance matrix, eigen decomposition, projection matrix", "resource": "Maths for ML Deisenroth Textbook", "url": "https://mml-book.github.io/book/mml-book.pdf" },
            { "id": 125, "title": "Unsupervised Learning Practice", "focus": "Solve 15 problems on PCA & clustering", "resource": "GATE Overflow ML Questions", "url": "https://gateoverflow.in/tag/machine-learning" },
            { "id": 126, "title": "Machine Learning Subject Test", "focus": "Solve 35 ML questions, log accuracy and weak spots", "resource": "GATE Overflow ML Questions", "url": "https://gateoverflow.in/tag/machine-learning" }
        ]
    },
    {
        "week": 19,
        "name": "AI Search Strategies",
        "phase": "phase3",
        "subject": "Artificial Intelligence",
        "days": [
            { "id": 127, "title": "Uninformed Search (BFS, DFS)", "focus": "BFS & DFS properties, time and space complexity, completeness", "resource": "GFG BFS vs DFS Comparison Guide", "url": "https://www.geeksforgeeks.org/difference-between-bfs-and-dfs/" },
            { "id": 128, "title": "Depth Limited & Iterative Deepening", "focus": "Space advantages of DFS with completeness of BFS", "resource": "GFG Iterative Deepening Search (IDS)", "url": "https://www.geeksforgeeks.org/dsa/iterative-deepening-searchids-iterative-deepening-depth-first-searchiddfs/" },
            { "id": 129, "title": "Informed Search (Greedy Best First)", "focus": "Heuristic functions, search tree expansion strategy", "resource": "GFG Greedy Best-First Search Guide", "url": "https://www.geeksforgeeks.org/greedy-best-first-search-algorithm/" },
            { "id": 130, "title": "A* Search", "focus": "A* completeness, heuristic admissibility (h(n) <= h*(n))", "resource": "GFG A* Search Algorithm Guide", "url": "https://www.geeksforgeeks.org/a-search-algorithm/" },
            { "id": 131, "title": "A* Consistency & Optimality", "focus": "Consistent heuristics, monotone property, optimality proofs", "resource": "Gate Applied A* Admissibility & Consistency Video", "url": "https://www.youtube.com/watch?v=CJmlP03ik5g" },
            { "id": 132, "title": "Minimax & Alpha-Beta Pruning", "focus": "Game trees, utility values, alpha-beta cutoffs", "resource": "CS188 Game Trees Note 02 (Minimax & Pruning)", "url": "https://inst.eecs.berkeley.edu/~cs188/fa23/assets/notes/cs188-fa23-note02.pdf" },
            { "id": 133, "title": "Search Algorithms Problems", "focus": "Solve game trees and calculate admissible A* heuristics", "resource": "GATE Overflow AI Questions", "url": "https://gateoverflow.in/tag/artificial-intelligence" }
        ]
    },
    {
        "week": 20,
        "name": "AI Logic & Uncertainty",
        "phase": "phase3",
        "subject": "Artificial Intelligence",
        "days": [
            { "id": 134, "title": "Propositional Logic Basics", "focus": "Conjunction, disjunction, implication, truth tables", "resource": "GFG Propositional Logic in AI Guide", "url": "https://www.geeksforgeeks.org/artificial-intelligence/propositional-logic-in-artificial-intelligence/" },
            { "id": 135, "title": "Propositional Inference", "focus": "Tautology, contradiction, resolution refutation proofs", "resource": "GFG Deductive Inference Rules & Deductions", "url": "https://www.geeksforgeeks.org/artificial-intelligence/deductive-reasoning-in-ai/" },
            { "id": 136, "title": "First-Order Logic (FOL)", "focus": "Quantifiers (Universal, Existential), predicates, functions", "resource": "GFG First-Order Logic in AI Guide", "url": "https://www.geeksforgeeks.org/artificial-intelligence/first-order-logic-in-artificial-intelligence/" },
            { "id": 137, "title": "FOL Inference & Unification", "focus": "Unification algorithm, Skolemization, resolution in FOL", "resource": "GFG Unification Algorithm in AI", "url": "https://www.geeksforgeeks.org/artificial-intelligence/unification-in-ai/" },
            { "id": 138, "title": "Bayesian Networks Syntax", "focus": "Graph structure, conditional probability tables (CPT)", "resource": "GFG Bayesian Belief Networks Guide", "url": "https://www.geeksforgeeks.org/machine-learning/basic-understanding-of-bayesian-belief-networks/" },
            { "id": 139, "title": "Bayesian Networks Independence", "focus": "d-separation active/inactive paths, joint factorization", "resource": "GFG Bayesian Belief Networks (d-Separation & Independence)", "url": "https://www.geeksforgeeks.org/machine-learning/basic-understanding-of-bayesian-belief-networks/" },
            { "id": 140, "title": "Artificial Intelligence Subject Test", "focus": "Complete AI subject test, check resolution and Bayes nets", "resource": "GATE Overflow AI Questions", "url": "https://gateoverflow.in/tag/artificial-intelligence" }
        ]
    },
    {
        "week": 21,
        "name": "General Aptitude & Math Revision",
        "phase": "phase4",
        "subject": "Revision",
        "days": [
            { "id": 141, "title": "Quantitative Aptitude (Ratios, %)", "focus": "Percentages, ratios, time-work, speed-distance", "resource": "GATE General Aptitude Resources", "url": "https://www.geeksforgeeks.org/gate-general-aptitude/" },
            { "id": 142, "title": "Aptitude Combinatorics & Stats", "focus": "Basic permutations, probability, mean-median-mode GA", "resource": "Saurabh Thakur GA Playlist (AptiXpress)", "url": "https://youtube.com/playlist?list=PLNEqvET0cb64A4pPR97wyMdHuZ8sN4VGr" },
            { "id": 143, "title": "Spatial Aptitude & Verbal", "focus": "Paper folding, shape rotations, English grammar, synonyms", "resource": "Saurabh Thakur GA Playlist (AptiXpress)", "url": "https://youtube.com/playlist?list=PLNEqvET0cb64A4pPR97wyMdHuZ8sN4VGr" },
            { "id": 144, "title": "Linear Algebra Formulas Review", "focus": "Four subspaces, eigenvalues, QR, SVD formula cards", "resource": "MIT Linear Algebra Lecture Notes (PDF)", "url": "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/4d876a9159e32543eb0d73b4d4382f4c_MIT18_06S10ZoomNotes.pdf" },
            { "id": 145, "title": "Probability Distributions Review", "focus": "Continuous/Discrete formula sheets, CLT bounds", "resource": "Probability Cheat Sheet (PDF)", "url": "https://wzchen.com/s/probability_cheatsheet.pdf" },
            { "id": 146, "title": "Calculus & Optimization Review", "focus": "Hessian matrix test, gradient descent update steps", "resource": "Lamar Calculus Cheat Sheet (PDF)", "url": "https://tutorial.math.lamar.edu/pdf/Calculus_Cheat_Sheet_All.pdf" },
            { "id": 147, "title": "Math & Aptitude Combined Test", "focus": "Take 40-question Math & GA combined mock test", "resource": "GATE Overflow General Aptitude", "url": "https://gateoverflow.in/tag/general-aptitude" }
        ]
    },
    {
        "week": 22,
        "name": "Core CS & ML/AI Revision",
        "phase": "phase4",
        "subject": "Revision",
        "days": [
            { "id": 148, "title": "Programming & Complexity Review", "focus": "Recursion trees, Master method, sorting bounds", "resource": "GeeksforGeeks Algorithms Guide", "url": "https://www.geeksforgeeks.org/fundamentals-of-algorithms/" },
            { "id": 149, "title": "Data Structures & Graphs Review", "focus": "Tree traversals, heap ops, Graph DFS/BFS codes", "resource": "GeeksforGeeks Data Structures Guide", "url": "https://www.geeksforgeeks.org/data-structures/" },
            { "id": 150, "title": "DBMS SQL & Normalization Review", "focus": "Checking normal forms, transactions serializability graphs", "resource": "GeeksforGeeks SQL Cheat Sheet", "url": "https://www.geeksforgeeks.org/sql-cheat-sheet/" },
            { "id": 151, "title": "Machine Learning Regression & SVM Review", "focus": "OLS formula, L1/L2 shapes, SVM margin formulas", "resource": "Stanford CS229 Supervised ML Cheat Sheet (PDF)", "url": "https://raw.githubusercontent.com/afshinea/stanford-cs-229-machine-learning/master/en/cheatsheet-supervised-learning.pdf" },
            { "id": 152, "title": "ML Trees & Neural Networks Review", "focus": "Information gain, backprop chain rule steps", "resource": "Stanford CS229 Supervised ML Cheat Sheet (PDF)", "url": "https://raw.githubusercontent.com/afshinea/stanford-cs-229-machine-learning/master/en/cheatsheet-supervised-learning.pdf" },
            { "id": 153, "title": "AI Search & Logic Review", "focus": "A* heuristics consistency, resolution rules FOL", "resource": "GFG Artificial Intelligence Tutorial", "url": "https://www.geeksforgeeks.org/artificial-intelligence/artificial-intelligence/" },
            { "id": 154, "title": "CS & ML/AI Combined Revision Test", "focus": "Take 40-question technical combined test", "resource": "GATE Overflow ML Questions", "url": "https://gateoverflow.in/tag/machine-learning" }
        ]
    },
    {
        "week": 23,
        "name": "Solve Official GATE DA PYQ Papers",
        "phase": "phase4",
        "subject": "Mock Prep",
        "days": [
            { "id": 155, "title": "Solve GATE DA 2024 - Part 1", "focus": "Attempt first 30 questions under 1.5 hours", "resource": "GO Classes GATE DA 2024 Solved Questions (Video)", "url": "https://www.youtube.com/watch?v=uzOmdiaYoSo" },
            { "id": 156, "title": "Solve GATE DA 2024 - Part 2", "focus": "Attempt remaining 35 questions", "resource": "GO Classes GATE DA 2024 Solved Questions (Video)", "url": "https://www.youtube.com/watch?v=uzOmdiaYoSo" },
            { "id": 157, "title": "Thorough Analysis of 2024 Paper", "focus": "Check solutions, write down wrong questions in Mistake Book", "resource": "GFG GATE DA 2024 Solved Paper Analysis", "url": "https://www.geeksforgeeks.org/gate/gate-da-important-questions/" },
            { "id": 158, "title": "Solve GATE DA 2025 - Part 1", "focus": "Attempt first 30 questions under exam conditions", "resource": "GO Classes GATE DA 2025 Solved Questions (Video)", "url": "https://www.youtube.com/watch?v=MGzuIszajAI" },
            { "id": 159, "title": "Solve GATE DA 2025 - Part 2", "focus": "Attempt remaining 35 questions", "resource": "GO Classes GATE DA 2025 Solved Questions (Video)", "url": "https://www.youtube.com/watch?v=MGzuIszajAI" },
            { "id": 160, "title": "Thorough Analysis of 2025 Paper", "focus": "Analyze error patterns, calculate total raw score", "resource": "GO Classes GATE DA 2025 Paper Analysis", "url": "https://www.youtube.com/watch?v=MGzuIszajAI" },
            { "id": 161, "title": "Mistake Book Sunday Review", "focus": "Re-solve all questions logged in your Mistake Book", "resource": "Personal Notes", "url": "" }
        ]
    },
    {
        "week": 24,
        "name": "Mock Tests & Short Notes Compile",
        "phase": "phase4",
        "subject": "Mock Prep",
        "days": [
            { "id": 162, "title": "Full Length Mock 1", "focus": "Attempt 3-hour mock. Focus on question selection", "resource": "🏆 Custom Premium Mock Exam (Take in Tab 4)", "url": "" },
            { "id": 163, "title": "Analyze Mock 1 & Revise", "focus": "Error analysis: mathematical slips vs conceptual gaps", "resource": "Personal Notes", "url": "" },
            { "id": 164, "title": "Full Length Mock 2", "focus": "Attempt 3-hour mock. Improve time allocation", "resource": "🏆 Custom Premium Mock Exam (Take in Tab 4)", "url": "" },
            { "id": 165, "title": "Analyze Mock 2 & Revise", "focus": "Review ML activation & backpropagation formulas", "resource": "Personal Notes", "url": "" },
            { "id": 166, "title": "Compile final 10-page Short Notes", "focus": "Extract core critical equations from all subjects", "resource": "Personal Notes", "url": "" },
            { "id": 167, "title": "Short Notes Review (Active Recall)", "focus": "Read title, write formulas without looking", "resource": "Personal Notes", "url": "" },
            { "id": 168, "title": "Weekly Rest & Mindset Tuning", "focus": "Light reading, rest, mental strategy outline", "resource": "Relaxation", "url": "" }
        ]
    },
    {
        "week": 25,
        "name": "Full Length Mock Exams - Batch 1",
        "phase": "phase4",
        "subject": "Mock Prep",
        "days": [
            { "id": 169, "title": "Full Length Mock 3", "focus": "Complete mock under simulated GATE timing (9 AM - 12 PM)", "resource": "🏆 Custom Premium Mock Exam (Take in Tab 4)", "url": "" },
            { "id": 170, "title": "Analyze Mock 3 & Target Revision", "focus": "Revise Bayesian nets and eigenvalues", "resource": "Personal Notes", "url": "" },
            { "id": 171, "title": "Full Length Mock 4", "focus": "Complete mock under simulated GATE timing", "resource": "🏆 Custom Premium Mock Exam (Take in Tab 4)", "url": "" },
            { "id": 172, "title": "Analyze Mock 4 & Target Revision", "focus": "Revise A* search heuristics conditions", "resource": "Personal Notes", "url": "" },
            { "id": 173, "title": "Full Length Mock 5", "focus": "Final score calibration mock", "resource": "🏆 Custom Premium Mock Exam (Take in Tab 4)", "url": "" },
            { "id": 174, "title": "Analyze Mock 5 & Review Mistakes", "focus": "Resolve final numeric calculations errors", "resource": "Personal Notes", "url": "" },
            { "id": 175, "title": "Sunday Revision of Short Notes", "focus": "Complete read-through of formula book", "resource": "Formula Book", "url": "" }
        ]
    },
    {
        "week": 26,
        "name": "Final Stretch (Days 176 - 180)",
        "phase": "phase4",
        "subject": "Final Stretch",
        "days": [
            { "id": 176, "title": "Final Formula Review", "focus": "Active recall on critical maths and ML parameters", "resource": "Short Notes Booklet", "url": "" },
            { "id": 177, "title": "Mistake Book Revision", "focus": "Read all logged mock test errors one last time", "resource": "Mistake Notebook", "url": "" },
            { "id": 178, "title": "No New Study / Light Review", "focus": "Read high-level NPTEL summary slides. Keep relaxed", "resource": "Relaxation", "url": "" },
            { "id": 179, "title": "Organize Exam Day Logistics", "focus": "Print Admit Card, review center guidelines, sleep early", "resource": "Exam Guidelines", "url": "" },
            { "id": 180, "title": "GATE EXAM DAY", "focus": "Stay calm, manage time carefully, crack the paper!", "resource": "Success Mindset", "url": "" }
        ]
    }
]

# Curated Resources
RESOURCES_CATALOG = [
    { "category": "math", "name": "GO Classes Linear Algebra for GATE DA", "type": "YouTube Playlist", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHhGLQ1ZT37KLpBMAD90CM4_" },
    { "category": "math", "name": "3Blue1Brown Essence of Linear Algebra", "type": "YouTube Visualizations", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab" },
    { "category": "math", "name": "GO Classes Probability for GATE DA/CS", "type": "MIT OpenCourseWare", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" },
    { "category": "math", "name": "GO Classes GATE DA Playlists", "type": "YouTube Channel", "url": "https://www.youtube.com/playlist?list=PLIPZ2_p3RNHjGbysj9OvLTfL2qhsTdsbr" },
    { "category": "math", "name": "Mathematics for Machine Learning Textbook", "type": "PDF / Free Book Chapters", "url": "https://mml-book.github.io/" },
    { "category": "math", "name": "3Blue1Brown Essence of Calculus", "type": "YouTube Playlist", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr" },
    { "category": "cs", "name": "NPTEL Programming & Data Structures in Python", "type": "NPTEL Course Lectures", "url": "https://nptel.ac.in/courses/106106145" },
    { "category": "cs", "name": "Amit Khurana DBMS Lectures", "type": "YouTube Playlist", "url": "https://tinyurl.com/AK-DBMS-GATE" },
    { "category": "cs", "name": "NPTEL Database System Concepts (IITM)", "type": "NPTEL Course", "url": "https://nptel.ac.in/courses/106105175" },
    { "category": "cs", "name": "GeeksforGeeks GATE CS & DA Notes", "type": "Written Tutorials", "url": "https://www.geeksforgeeks.org/gate-ds-ai-syllabus/" },
    { "category": "ml-ai", "name": "Stanford Andrew Ng CS229 Machine Learning", "type": "YouTube Playlist", "url": "https://www.youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU" },
    { "category": "ml-ai", "name": "NPTEL Introduction to Machine Learning (IITM)", "type": "NPTEL Course Lectures", "url": "https://nptel.ac.in/courses/106106139" },
    { "category": "ml-ai", "name": "UC Berkeley CS188 Artificial Intelligence", "type": "UC Berkeley Course Website", "url": "https://inst.eecs.berkeley.edu/~cs188/fa23/" },
    { "category": "ml-ai", "name": "NPTEL Artificial Intelligence Search Methods", "type": "NPTEL Course", "url": "https://nptel.ac.in/courses/106105077" },
    { "category": "ml-ai", "name": "3Blue1Brown Neural Networks Intuition", "type": "YouTube Videos", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000DX_ZCJB-3Ky" },
    { "category": "ml-ai", "name": "GATE Overflow Discussion Hub", "type": "GitHub Repository", "url": "https://gateoverflow.in/" }
]

SYLLABUS_SECTIONS = {
    "Linear Algebra": [
        ("la-1", "Vector Spaces, Subspaces"),
        ("la-2", "Linear independence, Span, Bases, Dimension"),
        ("la-3", "Linear transformations, Kernel, Range"),
        ("la-4", "Matrices, Systems of linear equations, Gauss elimination"),
        ("la-5", "Eigenvalues and Eigenvectors, Diagonalization"),
        ("la-6", "LU Decomposition, QR Decomposition, SVD")
    ],
    "Probability & Statistics": [
        ("stats-1", "Sample Space, Events, Axioms, Permutations & Combinations"),
        ("stats-2", "Conditional Probability, Bayes Theorem, Independence"),
        ("stats-3", "Random Variables PMF, PDF, CDF, Expectation, Variance"),
        ("stats-4", "Binomial, Poisson, Exponential, Uniform, Normal distributions"),
        ("stats-5", "Joint distributions, Marginal, Conditional, Covariance, Correlation"),
        ("stats-6", "Chebyshev inequality, Law of Large Numbers, Central Limit Theorem"),
        ("stats-7", "Estimation (Point, MLE, Bias, MSE), Sampling distributions"),
        ("stats-8", "Hypothesis testing: Z-test, T-test, Chi-square, p-values, errors")
    ],
    "Calculus & Optimization": [
        ("calc-1", "Limits, Continuity, Differentiability (Single variable)"),
        ("calc-2", "Mean Value Theorems, Taylor Series"),
        ("calc-3", "Maxima & Minima (Single variable)"),
        ("calc-4", "Multivariable calculus, Partial derivatives, Gradient, Hessian"),
        ("calc-5", "Unconstrained Optimization, Gradient Descent, local/global minima")
    ],
    "Programming, DSA (Python)": [
        ("dsa-1", "Python Programming (Syntax, collections, functions)"),
        ("dsa-2", "Algorithmic Complexity (Big-O, Theta, Omega, recursion)"),
        ("dsa-3", "Stacks, Queues, Linked Lists"),
        ("dsa-4", "Trees, Binary Search Trees, Binary Heaps"),
        ("dsa-5", "Graphs (representation, BFS, DFS)"),
        ("dsa-6", "Searching (Linear, Binary), Sorting algorithms")
    ],
    "DBMS & Data Warehousing": [
        ("dbms-1", "ER-Model, Relational model, Keys, Algebra"),
        ("dbms-2", "Relational Query Language: SQL queries, joins, subqueries"),
        ("dbms-3", "Functional Dependencies, Normalization (1NF, 2NF, 3NF, BCNF)"),
        ("dbms-4", "File Organization, Indexing (B-trees, B+ trees)"),
        ("dbms-5", "Transactions, ACID, serializability, Concurrency"),
        ("dbms-6", "Data Warehousing: Star/Snowflake schemas, OLAP operations")
    ],
    "Machine Learning": [
        ("ml-1", "ML Basics: Overfitting, Bias-Variance, Cross-validation"),
        ("ml-2", "Linear Regression, Ridge & Lasso Regularization"),
        ("ml-3", "Logistic Regression, classification evaluation metrics"),
        ("ml-4", "Support Vector Machines (SVM), Kernel trick"),
        ("ml-5", "Decision Trees (Entropy, Gini), Naive Bayes, KNN"),
        ("ml-6", "Multilayer Perceptron, Backpropagation, NN activation"),
        ("ml-7", "Clustering: K-means, K-medoids, Hierarchical clustering"),
        ("ml-8", "Principal Component Analysis (PCA)")
    ],
    "Artificial Intelligence": [
        ("ai-1", "Search: BFS, DFS, Iterative Deepening"),
        ("ai-2", "Informed Search: A*, Greedy Best First search"),
        ("ai-3", "Adversarial Search: Minimax, Alpha-Beta Pruning"),
        ("ai-4", "Logic: Propositional & First-Order logic, Truth Tables"),
        ("ai-5", "Reasoning under uncertainty: Bayesian Networks")
    ]
}

# ==========================================
# 2. File Database Persistence
# ==========================================
STORAGE_FILE = "progress.json"

def load_progress():
    default_state = {
        "completed_days": [],
        "daily_reviews": {},
        "syllabus_checked": [],
        "mocks": [],
        "is_premium_unlocked": False
    }
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r") as f:
                saved = json.load(f)
                # Assure dictionary structure matches
                for key in default_state:
                    if key not in saved:
                        saved[key] = default_state[key]
                return saved
        except Exception:
            return default_state
    return default_state

def save_progress(state):
    try:
        with open(STORAGE_FILE, "w") as f:
            json.dump(state, f, indent=4)
    except Exception as e:
        st.error(f"Error saving progress database: {e}")

# Load storage into Streamlit Session State
if "state" not in st.session_state:
    st.session_state.state = load_progress()

state = st.session_state.state

# Helper to save changes
def commit_changes():
    save_progress(st.session_state.state)

# ==========================================
# 3. Dynamic Aggregated Statistics
# ==========================================
total_days = 180
completed_count = len(state["completed_days"])
progress_pct = round((completed_count / total_days) * 100) if total_days > 0 else 0

total_hours = sum(float(log.get("hours", 0)) for log in state["daily_reviews"].values())

all_ratings = [int(log.get("rating", 5)) for log in state["daily_reviews"].values() if "rating" in log]
avg_confidence = round(sum(all_ratings) / len(all_ratings), 1) if all_ratings else 0.0

# Calculate streak
streak = 0
if state["completed_days"]:
    sorted_days = sorted([int(d) for d in state["completed_days"]], reverse=True)
    expected = sorted_days[0]
    streak = 1
    for day in sorted_days[1:]:
        if day == expected - 1:
            streak += 1
            expected = day
        else:
            break

# ==========================================
# 3.5. Authentication Guard & Login Interface
# ==========================================
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

if not st.session_state.is_logged_in:
    # Google Fonts
    st.markdown("<link href='https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Inter:wght@300;400;500;700&display=swap' rel='stylesheet'>", unsafe_allow_html=True)
    
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0d0f1d 0%, #151825 100%) !important;
            font-family: 'Inter', sans-serif !important;
        }
        div[data-testid="stForm"] {
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            background-color: rgba(15, 18, 37, 0.45) !important;
            backdrop-filter: blur(15px);
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        }
    </style>
    """, unsafe_allow_html=True)
    
    _, col_login, _ = st.columns([1, 1.8, 1])
    with col_login:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; margin-bottom: 25px;'>
            <h1 style='margin:0; font-family:"Outfit",sans-serif; font-weight:800; font-size:2.2rem; background: linear-gradient(to right, #00f2fe, #ab64fa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                🎓 GATE DA Study Companion
            </h1>
            <p style='margin: 8px 0 0 0; color: #8c9bb4; font-size:14px; font-family:"Inter",sans-serif;'>
                Secure topper-grade study path, revision logs, and interactive mock exams.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("<h4 style='margin-top:0; color:#f0f2f5; font-family:"Outfit",sans-serif;'>🔑 Secure Login</h4>", unsafe_allow_html=True)
            username = st.text_input("Email Address / Username", placeholder="e.g. admin@gate.in")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            
            submitted = st.form_submit_button("🔓 Sign In", type="primary", use_container_width=True)
            if submitted:
                if username.strip() == "admin@gate.in" and password == "gate2026":
                    st.session_state.is_logged_in = True
                    st.success("Access granted! Loading companion...")
                    st.rerun()
                elif not username or not password:
                    st.error("Please fill in both fields.")
                else:
                    st.error("Invalid credentials. Try the demo credentials below.")
                    
        st.markdown("""
        <div style="background-color: rgba(0, 242, 254, 0.05); border: 1px solid rgba(0, 242, 254, 0.15); border-radius: 10px; padding: 15px; margin-top: 15px; font-family:'Inter',sans-serif;">
            <span style="color:#00f2fe; font-weight:bold; font-size:13px;">💡 Demo Access Credentials:</span>
            <p style="margin: 5px 0 0 0; font-size:12px; color:#8c9bb4;">
                <strong>Email:</strong> admin@gate.in<br>
                <strong>Password:</strong> gate2026
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    st.stop()

# ==========================================
# 4. Premium Interface Layout & CSS Injection
# ==========================================
st.markdown("""
<style>
    /* Google Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Inter:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
    }
    
    /* Stats Metric Styling */
    div[data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 2.2rem;
        background: linear-gradient(135deg, #00f2fe, #8e2de2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Expander Layout */
    .st-emotion-cache-p5msec {
        background-color: rgba(15, 18, 37, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
    }
    
    /* Calendar Matrix styles */
    .matrix-grid {
        display: grid;
        grid-template-columns: repeat(30, 1fr);
        gap: 5px;
        margin-top: 15px;
    }
    .matrix-cell {
        aspect-ratio: 1;
        border-radius: 3px;
        position: relative;
        cursor: pointer;
        border: 1px solid rgba(255, 255, 255, 0.03);
    }
    .cell-empty { background: rgba(255, 255, 255, 0.04); }
    .cell-low { background: #b01c6c; }
    .cell-medium { background: #d05335; }
    .cell-high { background: #009624; }
    
    /* Header Gradient Banner */
    .header-banner {
        background: linear-gradient(135deg, rgba(142, 45, 226, 0.15) 0%, rgba(0, 242, 254, 0.15) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 25px;
        backdrop-filter: blur(10px);
    }
    
    /* Custom tags */
    .subject-badge {
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
    }
    .badge-math { background-color: rgba(0, 242, 254, 0.12); color: #00f2fe; }
    .badge-cs { background-color: rgba(171, 100, 250, 0.12); color: #ab64fa; }
    .badge-ml { background-color: rgba(0, 230, 118, 0.12); color: #00e676; }
    .badge-ai { background-color: rgba(255, 213, 79, 0.12); color: #ffd54f; }
    
    /* Disable the brightness dimming/opacity fading effect during execution reruns */
    [data-testid="stAppViewContainer"], 
    [data-testid="stAppViewBlockContainer"], 
    [data-testid="element-container"],
    div.element-container,
    [data-testid="stVerticalBlock"] > div,
    .stApp, 
    .main, 
    .block-container {
        opacity: 1 !important;
        filter: none !important;
        transition: none !important;
    }
</style>
""", unsafe_allow_html=True)

# App Header Banner
st.markdown(f"""
<div class="header-banner">
    <h1 style='margin:0; font-weight:800; font-size:2rem; background: linear-gradient(to right, #f0f2f5, #8c9bb4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        🎓 GATE Data Science & AI (DA) Study Companion
    </h1>
    <p style='margin: 8px 0 0 0; color: #8c9bb4; font-size:14px;'>
        Track your 6-month study path, log daily understanding analytics, search free resources, and log mock scores.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. Sidebar Statistics Display
# ==========================================
with st.sidebar:
    st.markdown("### 📊 Overall Status")
    
    # Progress Circle/Metric
    st.metric("Course Progress", f"{progress_pct}%", f"{completed_count} / {total_days} Days")
    
    # Progress bar filling
    st.progress(progress_pct / 100)
    
    st.markdown("---")
    
    # Metrics columns in sidebar
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Study Streak", f"{streak} Days", "🔥 active")
    with col2:
        st.metric("Total Hours", f"{round(total_hours, 1)} hrs", "⏱️ logged")
        
    st.metric("Avg. Confidence", f"{avg_confidence} / 5", "🧠 understanding")
    
    st.markdown("---")
    st.markdown("### 🏆 Topper Tips")
    st.info("""
    - **Math is King**: Vector Spaces & Probability hold 30%+ weightage.
    - **Mistake Book**: Log every wrong mock test question. Read it every Sunday.
    - **Active Recall**: Don't just read notes. Cover notes and write formulas from memory.
    """)
    
    st.markdown("[Printable Markdown Datasheet](file:///d:/roadmap%20for%20gaatt/datasheet.md)")
    
    st.markdown("---")
    st.markdown("### ⚙️ Reset Options")
    with st.popover("⚠️ Reset Study Data"):
        st.warning("This will permanently erase all completed days, logged hours, syllabus progress, and mock scores.")
        confirm_code = st.text_input("Type 'RESET' to confirm:", key="reset_confirm")
        if st.button("Permanently Reset App", type="primary", key="reset_btn"):
            if confirm_code.strip().upper() == "RESET":
                st.session_state.state = {
                    "completed_days": [],
                    "daily_reviews": {},
                    "syllabus_checked": [],
                    "mocks": []
                }
                save_progress(st.session_state.state)
                st.success("App data has been reset!")
                st.rerun()
            else:
                st.error("Please type 'RESET' to confirm.")
                
    st.markdown("---")
    if st.button("🚪 Sign Out", use_container_width=True, key="sign_out_btn"):
        st.session_state.is_logged_in = False
        st.rerun()

# ==========================================
# 6. Tabbed View Navigation
# ==========================================
tabs = st.tabs(["📈 Performance Analytics", "📅 Study Planner", "📋 Syllabus Tracker", "📚 Free Resources", "📝 Mock Tests Log"])

# ------------------------------------------
# Tab 1: Study Planner
# ------------------------------------------
with tabs[1]:
    col_hdr, col_fltr = st.columns([2, 1])
    with col_hdr:
        st.subheader("180-Day Study Plan")
        st.caption("Tick off each day as you finish studying. Expand to log your study duration, notes, and confidence rate.")
        
    with col_fltr:
        phase_filter = st.selectbox("Select Phase Filter:", [
            "All (180 Days)",
            "Phase 1: Mathematical Foundations (Days 1-70)",
            "Phase 2: CS & Databases (Days 71-98)",
            "Phase 3: AI & Machine Learning (Days 99-140)",
            "Phase 4: Revision & Mocks (Days 141-180)"
        ])
        
    # Map selection value to filter key
    phase_key = "all"
    if "Phase 1" in phase_filter: phase_key = "phase1"
    elif "Phase 2" in phase_filter: phase_key = "phase2"
    elif "Phase 3" in phase_filter: phase_key = "phase3"
    elif "Phase 4" in phase_filter: phase_key = "phase4"

    # Render accordion list of weeks
    for week_obj in STUDY_PLAN:
        if phase_key != "all" and week_obj["phase"] != phase_key:
            continue
            
        completed_week_days = [d["id"] for d in week_obj["days"] if d["id"] in state["completed_days"]]
        pct_week = round((len(completed_week_days) / len(week_obj["days"])) * 100)
        
        expander_title = f"Week {week_obj['week']}: {week_obj['name']} ({week_obj['subject']}) — {len(completed_week_days)}/{len(week_obj['days'])} Completed ({pct_week}%)"
        
        with st.expander(expander_title, expanded=(week_obj["week"] == 1)):
            for day in week_obj["days"]:
                day_id = day["id"]
                day_id_str = str(day_id)
                
                # Check status
                is_done = day_id in state["completed_days"]
                
                # Create row elements
                col_chk, col_info, col_log = st.columns([0.2, 2.5, 1.5])
                
                with col_chk:
                    # Checkbox for day completion
                    checked = st.checkbox("", value=is_done, key=f"chk_{day_id}")
                    if checked != is_done:
                        if checked:
                            if day_id not in state["completed_days"]:
                                state["completed_days"].append(day_id)
                        else:
                            state["completed_days"] = [d for d in state["completed_days"] if d != day_id]
                            if day_id_str in state["daily_reviews"]:
                                del state["daily_reviews"][day_id_str]
                        commit_changes()
                        st.rerun()
                        
                with col_info:
                    st.markdown(f"**Day {day_id}: {day['title']}**")
                    st.markdown(f"<span style='font-size:12px; color:#8c9bb4;'><strong>Focus:</strong> {day['focus']}</span>", unsafe_allow_html=True)
                    if day['url']:
                        st.markdown(f"[🔗 Resource: {day['resource']}]({day['url']})")
                    if day_id in [166, 167, 175, 176]:
                        try:
                            with open("short_notes.md", "r", encoding="utf-8") as f:
                                short_notes_md = f.read()
                            st.download_button(
                                label="📥 Download GATE DA Short Notes (Free)",
                                data=short_notes_md,
                                file_name="GATE_DA_Short_Notes.md",
                                mime="text/markdown",
                                key=f"dl_notes_{day_id}"
                            )
                        except Exception as e:
                            pass
                        
                with col_log:
                    # Log review input fields directly inline
                    if checked:
                        # Get existing review details
                        review = state["daily_reviews"].get(day_id_str, {"hours": 5.5, "rating": 5, "notes": ""})
                        
                        # Trigger popovers or inline form inputs
                        with st.popover("📝 Log / Edit Review"):
                            st.markdown(f"##### Log Review - Day {day_id}")
                            logged_hours = st.number_input("Hours Spent", min_value=0.0, max_value=24.0, value=float(review.get("hours", 5.5)), step=0.25, key=f"hrs_{day_id}")
                            logged_rating = st.slider("Understanding Rating (1=Weak, 5=Expert)", min_value=1, max_value=5, value=int(review.get("rating", 5)), key=f"rat_{day_id}")
                            logged_notes = st.text_area("Daily Notes / Observations", value=review.get("notes", ""), placeholder="e.g. eigenvalues formula was easy, but struggled with QR projections", key=f"note_{day_id}")
                            
                            if st.button("Save Log", key=f"btn_save_{day_id}"):
                                state["daily_reviews"][day_id_str] = {
                                    "hours": logged_hours,
                                    "rating": logged_rating,
                                    "notes": logged_notes
                                }
                                commit_changes()
                                st.success("Review logged!")
                                st.rerun()
                                
                        # Display status badges
                        if day_id_str in state["daily_reviews"]:
                            rev_data = state["daily_reviews"][day_id_str]
                            st.markdown(f"<span class='subject-badge badge-ml'>{rev_data['rating']}★ Rated</span> <span class='subject-badge badge-math'>{rev_data['hours']} hrs</span>", unsafe_allow_html=True)
                            if rev_data["notes"]:
                                st.markdown(f"<p style='font-size:11px; font-style:italic; color:#5e6b82; margin:0;'>Notes: {rev_data['notes'][:60]}...</p>", unsafe_allow_html=True)
                        else:
                            st.markdown("<span style='font-size:12px; color:#ff7e5f; font-style:italic;'>No review logged yet</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='font-size:12px; color:#5e6b82;'>Check off day to log review</span>", unsafe_allow_html=True)
                
                                # Inline Mock Test for Day 162, 164, 169, 171, 173 (Week 24 & Week 25)
                if day_id in [162, 164, 169, 171, 173]:
                    is_free_mock = day_id in [162, 164]
                    is_unlocked = state.get("is_premium_unlocked", False) or is_free_mock
                    
                    if not is_unlocked:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, rgba(255, 126, 95, 0.08) 0%, rgba(254, 180, 123, 0.08) 100%); 
                                    border: 1px dashed rgba(255, 126, 95, 0.25); border-radius: 8px; padding: 12px; margin: 10px 0 10px 30px;">
                            <span style="color:#ff7e5f; font-weight:bold; font-size:13px;">🔒 Premium Mock Test is Locked</span>
                            <p style="margin: 5px 0 10px 0; font-size:11px; color:#8c9bb4;">Mock 1, 2, and 3 are completely free! Pay a one-time fee of ₹10 via UPI to unlock Mock 4 and Mock 5 (Full-Length & Subject Exams).</p>
                        </div>
                        """, unsafe_allow_html=True)
                        col_pad, col_unlock_btn = st.columns([0.15, 3.85])
                        with col_unlock_btn:
                            with st.popover("🔓 Unlock All Mock Exams (₹10)"):
                                st.image("upi_qr.png", caption="Scan using GPay, PhonePe, Paytm, etc. to Pay ₹10", width=180)
                                st.success("UPI ID: 6376541591@fam")
                                utr_input = st.text_input("Enter 12-digit UPI Ref/UTR No. after payment:", placeholder="e.g. 620584739201", key=f"utr_{day_id}")
                                if st.button("🚀 Verify & Unlock", type="primary", key=f"pay_inline_{day_id}"):
                                    if not utr_input:
                                        st.error("Please enter the 12-digit UTR/Ref No.")
                                    elif len(utr_input) != 12 or not utr_input.isdigit():
                                        st.error("Invalid UTR. The UPI Ref No. must be exactly 12 numeric digits.")
                                    else:
                                        import time
                                        with st.spinner("Connecting to UPI networks to verify transaction..."):
                                            time.sleep(2)
                                        state["is_premium_unlocked"] = True
                                        commit_changes()
                                        st.balloons()
                                        st.success("🎉 All Mock Exams Unlocked!")
                                        st.rerun()
                    else:
                        # Render interactive quiz
                        exam_id = f"premium_mock_{day_id}"
                        
                        # Set titles
                        if day_id == 162:
                            exam_name = "Mock Exam 1: GATE DA Full-Length Prediction Mock"
                        elif day_id == 164:
                            exam_name = "Mock Exam 2: Advanced AI, ML & Math Subject Mock"
                        elif day_id == 169:
                            exam_name = "Mock Exam 3: Linear Algebra, ML & Calculus Mock"
                        elif day_id == 171:
                            exam_name = "Mock Exam 4: Deep Learning & Propositional Logic Mock"
                        else:
                            exam_name = "Mock Exam 5: AI Heuristics, PCA & Probability Mock"
                            
                        # Load questions dataset
                        if day_id == 162:
                            INLINE_QUESTIONS = [
                                {
                                    "id": "q1",
                                    "type": "MCQ",
                                    "question": "Let $A$ be a $3 \\times 3$ matrix with eigenvalues $1, 2, 3$. What is the determinant of the matrix $B = A^2 - A$?",
                                    "options": ["A) 0", "B) 6", "C) 12", "D) 18"],
                                    "correct": "A) 0",
                                    "explanation": "The eigenvalues of $A$ are $\\lambda_1 = 1$, $\\lambda_2 = 2$, and $\\lambda_3 = 3$.\n\n"
                                                   "The eigenvalues of the matrix $B = A^2 - A$ are given by $f(\\lambda_i) = \\lambda_i^2 - \\lambda_i$:\n"
                                                   "- For $\\lambda_1 = 1$: $1^2 - 1 = 0$\n"
                                                   "- For $\\lambda_2 = 2$: $2^2 - 2 = 2$\n"
                                                   "- For $\\lambda_3 = 3$: $3^2 - 3 = 6$\n\n"
                                                   "The determinant of a matrix is the product of its eigenvalues. Therefore, $\\text{det}(B) = 0 \\times 2 \\times 6 = 0$. Thus, Option A is correct."
                                },
                                {
                                    "id": "q2",
                                    "type": "MSQ",
                                    "question": "Which of the following statements are **TRUE** regarding Artificial Intelligence search algorithms? (Select all that apply)",
                                    "options": [
                                        "A) A* search is optimal if the heuristic function $h(n)$ is admissible for tree search.",
                                        "B) Uniform Cost Search (UCS) is optimal and complete if step costs are strictly positive.",
                                        "C) A consistent heuristic is always admissible.",
                                        "D) Depth-First Search (DFS) has a worst-case space complexity of $O(b^d)$ where $b$ is the branching factor and $d$ is the depth."
                                    ],
                                    "correct": ["A) A* search is optimal if the heuristic function $h(n)$ is admissible for tree search.", 
                                                "B) Uniform Cost Search (UCS) is optimal and complete if step costs are strictly positive.", 
                                                "C) A consistent heuristic is always admissible."],
                                    "explanation": "Let's analyze the statements:\n"
                                                   "- **A is TRUE**: Admissibility of $h(n)$ guarantees optimality in tree search.\n"
                                                   "- **B is TRUE**: UCS is a special case of Dijkstra's algorithm; it is complete and optimal if step costs $\\ge \\epsilon > 0$.\n"
                                                   "- **C is TRUE**: Consistency ($h(n) \\le c(n, a, n') + h(n')$) is a stronger condition than admissibility; all consistent heuristics are admissible.\n"
                                                   "- **D is FALSE**: DFS has a space complexity of $O(bd)$ in the worst case, not $O(b^d)$. (BFS has $O(b^d)$ space complexity)."
                                },
                                {
                                    "id": "q3",
                                    "type": "NAT",
                                    "question": "Consider a Naive Bayes classifier with two classes $C_1$ and $C_2$. The prior probability is $P(C_1) = 0.6$. "
                                                "For a binary feature $X$, the conditional probabilities are $P(X=1 \\mid C_1) = 0.3$ and $P(X=1 \\mid C_2) = 0.8$. "
                                                "Compute the posterior probability $P(C_1 \\mid X=1)$. (Enter your answer rounded off to 2 decimal places, e.g. 0.36)",
                                    "correct": 0.36,
                                    "tolerance": 0.01,
                                    "explanation": "By Bayes' Theorem:\n"
                                                   "$$P(C_1 \\mid X=1) = \\frac{P(X=1 \\mid C_1) P(C_1)}{P(X=1)}$$\n\n"
                                                   "First, calculate the marginal probability $P(X=1)$ using the law of total probability:\n"
                                                   "$$P(X=1) = P(X=1 \\mid C_1)P(C_1) + P(X=1 \\mid C_2)P(C_2)$$\n"
                                                   "Given $P(C_1) = 0.6 \\implies P(C_2) = 1 - 0.6 = 0.4$:\n"
                                                   "$$P(X=1) = (0.3 \\times 0.6) + (0.8 \\times 0.4) = 0.18 + 0.32 = 0.50$$\n\n"
                                                   "Now, substitute back into Bayes' formula:\n"
                                                   "$$P(C_1 \\mid X=1) = \\frac{0.18}{0.50} = 0.36$$"
                                },
                                {
                                    "id": "q4",
                                    "type": "MCQ",
                                    "question": "Let $R(A, B, C, D, E)$ be a relational schema with functional dependencies: $A \\to B$, $B \\to C$, and $D \\to E$. "
                                                "Which of the following is the candidate key for $R$?",
                                    "options": ["A) A", "B) AD", "C) ADE", "D) ABD"],
                                    "correct": "B) AD",
                                    "explanation": "To find the candidate key, we compute the closure of attributes:\n"
                                                   "- $\\{A\\}^+ = \\{A, B, C\\}$ (does not contain $D, E$)\n"
                                                   "- $\\{AD\\}^+ = \\{A, D\\}^+$\n"
                                                   "  Using $A \\to B$: $\\{A, D, B\\}$\n"
                                                   "  Using $B \\to C$: $\\{A, D, B, C\\}$ \n"
                                                   "  Using $D \\to E$: $\\{A, D, B, C, E\\}$ = all attributes of relation $R$.\n\n"
                                                   "Since $\\{AD\\}^+$ contains all attributes and no proper subset of $\\{AD\\}$ is a superkey, $AD$ is the candidate key."
                                },
                                {
                                    "id": "q5",
                                    "type": "NAT",
                                    "question": "The probability density function of a continuous random variable $X$ is given by $f(x) = k x^2$ for $0 \\le x \\le 2$, and $f(x) = 0$ otherwise. "
                                                "Calculate the value of the constant $k$. (Enter your answer as a decimal rounded off to 3 decimal places, e.g. 0.375)",
                                    "correct": 0.375,
                                    "tolerance": 0.005,
                                    "explanation": "Since $f(x)$ is a probability density function, the total area under the curve must equal 1:\n"
                                                   "$$\\int_{-\\infty}^{\\infty} f(x) dx = 1 \\implies \\int_0^2 k x^2 dx = 1$$\n\n"
                                                   "Perform the integration:\n"
                                                   "$$k \\left[ \\frac{x^3}{3} \\right]_0^2 = 1 \\implies k \\left( \\frac{8}{3} - 0 \\right) = 1$$\n"
                                                   "$$k \\frac{8}{3} = 1 \\implies k = \\frac{3}{8} = 0.375$$"
                                }
                            ]
                        elif day_id == 164:
                            INLINE_QUESTIONS = [
                                {
                                    "id": "q1",
                                    "type": "MCQ",
                                    "question": "Let $X$ and $Y$ be independent Poisson random variables with parameters $\\lambda_1 = 2$ and $\\lambda_2 = 3$ respectively. "
                                                "What is the probability $P(X + Y = 1)$?",
                                    "options": ["A) $e^{-5}$", "B) $5e^{-5}$", "C) $6e^{-5}$", "D) $2.5e^{-5}$"],
                                    "correct": "B) $5e^{-5}$",
                                    "explanation": "Since $X$ and $Y$ are independent Poisson random variables with parameters $\\lambda_1$ and $\\lambda_2$, their sum $Z = X + Y$ is also a Poisson random variable with parameter $\\lambda = \\lambda_1 + \\lambda_2 = 2 + 3 = 5$.\n\n"
                                                   "The probability mass function of a Poisson random variable is $P(Z = z) = \\frac{e^{-\\lambda} \\lambda^z}{z!}$.\n\n"
                                                   "For $z = 1$:\n"
                                                   "$$P(X + Y = 1) = \\frac{e^{-5} 5^1}{1!} = 5e^{-5}$$"
                                },
                                {
                                    "id": "q2",
                                    "type": "MSQ",
                                    "question": "Which of the following are **TRUE** regarding support vector machines (SVM)? (Select all that apply)",
                                    "options": [
                                        "A) In a soft-margin SVM, the parameter $C$ controls the trade-off between margin size and classification errors.",
                                        "B) If we increase $C$, the margin size decreases and the classifier becomes more prone to overfitting.",
                                        "C) The dual formulation of SVM optimization depends only on the dot products of input feature vectors.",
                                        "D) The radial basis function (RBF) kernel maps the inputs to a finite-dimensional feature space."
                                    ],
                                    "correct": ["A) In a soft-margin SVM, the parameter $C$ controls the trade-off between margin size and classification errors.",
                                                "B) If we increase $C$, the margin size decreases and the classifier becomes more prone to overfitting.",
                                                "C) The dual formulation of SVM optimization depends only on the dot products of input feature vectors."],
                                    "explanation": "- **A is TRUE**: $C$ regulates regularization. High $C$ prioritizes correct classification, small $C$ prioritizes a wider margin.\n"
                                                   "- **B is TRUE**: High $C$ fits training data very strictly, shrinking the margin, leading to overfitting risk.\n"
                                                   "- **C is TRUE**: The dual objective function involves $\\sum \\alpha_i \\alpha_j y_i y_j (x_i \\cdot x_j)$, enabling the kernel trick.\n"
                                                   "- **D is FALSE**: The RBF kernel maps inputs to an *infinite*-dimensional feature space, not finite."
                                },
                                {
                                    "id": "q3",
                                    "type": "NAT",
                                    "question": "Assume we run the K-Means algorithm on a 1D dataset containing points $\\{2, 4, 10, 12, 20\\}$ with $K = 2$. "
                                                "The initial centroids are chosen as $c_1 = 3$ and $c_2 = 15$. "
                                                "What is the value of the updated centroid $c_1$ after the first iteration? (Enter your answer as a single integer/decimal)",
                                    "correct": 3.0,
                                    "tolerance": 0.01,
                                    "explanation": "Let's run the first assignment step:\n"
                                                   "- Point 2: distance to $c_1(3)$ is 1, distance to $c_2(15)$ is 13. Assign to Cluster 1.\n"
                                                   "- Point 4: distance to $c_1(3)$ is 1, distance to $c_2(15)$ is 11. Assign to Cluster 1.\n"
                                                   "- Point 10: distance to $c_1(3)$ is 7, distance to $c_2(15)$ is 5. Assign to Cluster 2.\n"
                                                   "- Point 12: distance to $c_1(3)$ is 9, distance to $c_2(15)$ is 3. Assign to Cluster 2.\n"
                                                   "- Point 20: distance to $c_1(3)$ is 17, distance to $c_2(15)$ is 5. Assign to Cluster 2.\n\n"
                                                   "Cluster 1 points: $\\{2, 4\\}$.\n"
                                                   "Cluster 2 points: $\\{10, 12, 20\\}$.\n\n"
                                                   "Updated centroid $c_1 = \\frac{2 + 4}{2} = 3.0$."
                                },
                                {
                                    "id": "q4",
                                    "type": "MCQ",
                                    "question": "Let $X$ be a random variable representing the height of students. We collect a sample of size $n = 100$ "
                                                "and calculate the sample mean $\\bar{x} = 170$ cm with sample standard deviation $s = 10$ cm. "
                                                "What is the approximate $95\\%$ confidence interval for the population mean? (Use $z_{0.025} = 1.96$)",
                                    "options": ["A) [169.02, 170.98]", "B) [168.04, 171.96]", "C) [165.02, 174.98]", "D) [167.08, 172.92]"],
                                    "correct": "B) [168.04, 171.96]",
                                    "explanation": "The formula for the confidence interval of the mean is:\n"
                                                   "$$\\bar{x} \\pm z \\frac{s}{\\sqrt{n}}$$\n\n"
                                                   "Substitute the given values:\n"
                                                   "- $\\bar{x} = 170$\n"
                                                   "- $z = 1.96$\n"
                                                   "- $s = 10$\n"
                                                   "- $n = 100 \\implies \\sqrt{n} = 10$\n\n"
                                                   "Calculate standard error:\n"
                                                   "$$\\text{SE} = \\frac{10}{10} = 1$$\n\n"
                                                   "Calculate margin of error:\n"
                                                   "$$\\text{ME} = 1.96 \\times 1 = 1.96$$\n\n"
                                                   "Thus, the interval is:\n"
                                                   "$$[170 - 1.96, 170 + 1.96] = [168.04, 171.96]$$"
                                },
                                {
                                    "id": "q5",
                                    "type": "NAT",
                                    "question": "Find the maximum value of the function $f(x) = -2x^2 + 8x + 5$ using optimization methods. "
                                                "(Enter your answer as a single integer/decimal)",
                                    "correct": 13.0,
                                    "tolerance": 0.01,
                                    "explanation": "To find the maximum, we calculate the first derivative and set it to zero:\n"
                                                   "$$f'(x) = -4x + 8 = 0 \\implies x = 2$$\n\n"
                                                   "Verify using the second derivative:\n"
                                                   "$$f''(x) = -4 < 0$$\n"
                                                   "Since the second derivative is negative, $x=2$ is a local and global maximum.\n\n"
                                                   "Substitute $x=2$ back into the original function $f(x)$:\n"
                                                   "$$f(2) = -2(2)^2 + 8(2) + 5 = -8 + 16 + 5 = 13.0$$"
                                }
                            ]
                        elif day_id == 169:
                            INLINE_QUESTIONS = [
                                {
                                    "id": "q1",
                                    "type": "MCQ",
                                    "question": "Consider a system of linear equations $Ax = b$ where $A$ is a $3 \\times 4$ matrix. Which of the following is true?",
                                    "options": [
                                        "A) The system always has a unique solution.",
                                        "B) If the rank of $A$ is 3, the system has infinitely many solutions.",
                                        "C) If $b=0$, the system has only the trivial solution $x=0$.",
                                        "D) The system can never be inconsistent."
                                    ],
                                    "correct": "B) If the rank of $A$ is 3, the system has infinitely many solutions.",
                                    "explanation": "Since $A$ has dimensions $3 \\times 4$, the system has 4 variables and 3 equations. "
                                                   "If the rank of $A$ is 3, there are 3 pivot variables and $4-3 = 1$ free variable. "
                                                   "Since there is a free variable, the system (if consistent) has infinitely many solutions. "
                                                   "Since the rank is 3 (equal to the number of rows), the column space of $A$ spans $\\mathbb{R}^3$, "
                                                   "so $Ax=b$ is always consistent for any $b \\in \\mathbb{R}^3$. Hence, it has infinitely many solutions."
                                },
                                {
                                    "id": "q2",
                                    "type": "MSQ",
                                    "question": "Which of the following properties are guaranteed by the ACID transaction model in DBMS? (Select all that apply)",
                                    "options": [
                                        "A) Atomicity: All operations in a transaction succeed or all fail.",
                                        "B) Consistency: A transaction transforms the database from one valid state to another.",
                                        "C) Isolation: Concurrent execution of transactions yields the same state as sequential execution.",
                                        "D) Durability: Once committed, updates survive system crashes."
                                    ],
                                    "correct": [
                                        "A) Atomicity: All operations in a transaction succeed or all fail.",
                                        "B) Consistency: A transaction transforms the database from one valid state to another.",
                                        "C) Isolation: Concurrent execution of transactions yields the same state as sequential execution.",
                                        "D) Durability: Once committed, updates survive system crashes."
                                    ],
                                    "explanation": "All four properties define ACID: Atomicity, Consistency, Isolation, and Durability."
                                },
                                {
                                    "id": "q3",
                                    "type": "NAT",
                                    "question": "Suppose we have a dataset with a single feature $x$ and target $y$. The linear regression model is $y = w x + b$. "
                                                "The data points are $(1, 2)$, $(2, 4)$, and $(3, 5)$. What is the optimal value of $w$ that minimizes the mean squared error? "
                                                "(Round off to 2 decimal places, e.g. 1.50)",
                                    "correct": 1.50,
                                    "tolerance": 0.01,
                                    "explanation": "Using the slope formula for simple linear regression:\n"
                                                   "$$w = \\frac{n \\sum xy - \\sum x \\sum y}{n \\sum x^2 - (\\sum x)^2}$$\n\n"
                                                   "Substitute the values:\n"
                                                   "- $n = 3$\n"
                                                   "- $\\sum x = 1 + 2 + 3 = 6$\n"
                                                   "- $\\sum y = 2 + 4 + 5 = 11$\n"
                                                   "- $\\sum x^2 = 1 + 4 + 9 = 14$\n"
                                                   "- $\\sum xy = (1\\times 2) + (2\\times 4) + (3\\times 5) = 2 + 8 + 15 = 25$\n\n"
                                                   "Calculate $w$:\n"
                                                   "$$w = \\frac{3(25) - 6(11)}{3(14) - 6^2} = \\frac{75 - 66}{42 - 36} = \\frac{9}{6} = 1.5$$"
                                },
                                {
                                    "id": "q4",
                                    "type": "MCQ",
                                    "question": "What is the value of the limit: $\\lim_{x \\to 0} \\frac{e^x - 1 - x}{x^2}$?",
                                    "options": ["A) 0", "B) 0.5", "C) 1", "D) Undefined"],
                                    "correct": "B) 0.5",
                                    "explanation": "Applying L'Hopital's Rule since the limit has a $0/0$ indeterminate form:\n"
                                                   "$$\\lim_{x \\to 0} \\frac{e^x - 1}{2x}$$\n"
                                                   "This is still $0/0$. Applying L'Hopital's Rule again:\n"
                                                   "$$\\lim_{x \\to 0} \\frac{e^x}{2} = \\frac{e^0}{2} = \\frac{1}{2} = 0.5$$"
                                },
                                {
                                    "id": "q5",
                                    "type": "NAT",
                                    "question": "The probability of hitting a target in any single shot is $0.4$. If 3 independent shots are fired, "
                                                "what is the probability that the target is hit at least once? (Round off to 3 decimal places, e.g. 0.784)",
                                    "correct": 0.784,
                                    "tolerance": 0.002,
                                    "explanation": "The probability of hitting the target at least once is $1$ minus the probability of missing it on all three shots.\n"
                                                   "Probability of missing a single shot is $1 - 0.4 = 0.6$.\n\n"
                                                   "Since shots are independent:\n"
                                                   "$$P(\\text{miss all 3}) = 0.6^3 = 0.216$$\n\n"
                                                   "Therefore:\n"
                                                   "$$P(\\text{hit at least once}) = 1 - 0.216 = 0.784$$"
                                }
                            ]
                        elif day_id == 171:
                            INLINE_QUESTIONS = [
                                {
                                    "id": "q1",
                                    "type": "MCQ",
                                    "question": "Which of the following activation functions can output negative values?",
                                    "options": ["A) Sigmoid", "B) ReLU", "C) Leaky ReLU", "D) Softmax"],
                                    "correct": "C) Leaky ReLU",
                                    "explanation": "Leaky ReLU is defined as $f(x) = \\max(\\alpha x, x)$ where $0 < \\alpha < 1$. For $x < 0$, $f(x) = \\alpha x$, which is negative. "
                                                   "Sigmoid outputs in $(0, 1)$, ReLU outputs in $[0, \\infty)$, and Softmax outputs probability values in $(0, 1)$."
                                },
                                {
                                    "id": "q2",
                                    "type": "MSQ",
                                    "question": "Which of the following are valid inference rules in propositional logic? (Select all that apply)",
                                    "options": [
                                        "A) Modus Ponens: From $P$ and $P \\to Q$, infer $Q$.",
                                        "B) Modus Tollens: From $\\neg Q$ and $P \\to Q$, infer $\\neg P$.",
                                        "C) Disjunctive Syllogism: From $P \\lor Q$ and $\\neg P$, infer $Q$.",
                                        "D) Affirming the Consequent: From $Q$ and $P \\to Q$, infer $P$."
                                    ],
                                    "correct": [
                                        "A) Modus Ponens: From $P$ and $P \\to Q$, infer $Q$.",
                                        "B) Modus Tollens: From $\\neg Q$ and $P \\to Q$, infer $\\neg P$.",
                                        "C) Disjunctive Syllogism: From $P \\lor Q$ and $\\neg P$, infer $Q$."
                                    ],
                                    "explanation": "A, B, and C are logically sound deductive rules. D is Affirming the Consequent, which is a formal logical fallacy."
                                },
                                {
                                    "id": "q3",
                                    "type": "NAT",
                                    "question": "Let relation $R(A, B, C)$ contain 10 tuples, and relation $S(C, D)$ contain 5 tuples. "
                                                "What is the maximum possible number of tuples in the natural join $R \\bowtie S$? (Assume no constraints)",
                                    "correct": 50,
                                    "tolerance": 0,
                                    "explanation": "The natural join combines tuples on the shared attribute $C$. In the worst-case scenario, "
                                                   "all 10 tuples in $R$ have the same value for attribute $C$ (e.g. $C=1$), and all 5 tuples "
                                                   "in $S$ also have that same value $C=1$. Under these conditions, every tuple of $R$ joins with "
                                                   "every tuple of $S$. The resulting table will contain $10 \\times 5 = 50$ tuples."
                                },
                                {
                                    "id": "q4",
                                    "type": "MCQ",
                                    "question": "If $A$ is a real symmetric matrix, which of the following is always true?",
                                    "options": ["A) All eigenvalues of $A$ are real.", "B) $A$ is always invertible.", "C) All eigenvalues of $A$ are positive.", "D) $A$ is always diagonal."],
                                    "correct": "A) All eigenvalues of $A$ are real.",
                                    "explanation": "By the Spectral Theorem, any real symmetric matrix has real eigenvalues. It is not necessarily invertible (eigenvalues can be zero), positive (eigenvalues can be negative), or diagonal (though it is diagonalizable)."
                                },
                                {
                                    "id": "q5",
                                    "type": "NAT",
                                    "question": "Two fair 6-sided dice are rolled. What is the probability that the sum of the numbers shown is 7? "
                                                "(Round off to 3 decimal places, e.g. 0.167)",
                                    "correct": 0.167,
                                    "tolerance": 0.002,
                                    "explanation": "Total possible outcomes from rolling two 6-sided dice is $6 \\times 6 = 36$.\n"
                                                   "Outcomes where sum equals 7:\n"
                                                   "$$\\{(1,6), (2,5), (3,4), (4,3), (5,2), (6,1)\\}$$\n"
                                                   "There are 6 successful outcomes.\n\n"
                                                   "Probability is:\n"
                                                   "$$P = \\frac{6}{36} = \\frac{1}{6} \\approx 0.167$$"
                                }
                            ]
                        else:
                            INLINE_QUESTIONS = [
                                {
                                    "id": "q1",
                                    "type": "MCQ",
                                    "question": "Which of the following search algorithms expands nodes in order of their $f(n) = g(n) + h(n)$ value?",
                                    "options": ["A) Breadth-First Search", "B) Uniform Cost Search", "C) Greedy Best-First Search", "D) A* Search"],
                                    "correct": "D) A* Search",
                                    "explanation": "A* search uses the evaluation function $f(n) = g(n) + h(n)$, where $g(n)$ is cost to reach node $n$ and $h(n)$ is heuristic estimate to target."
                                },
                                {
                                    "id": "q2",
                                    "type": "MSQ",
                                    "question": "Which of the following are common techniques used to prevent overfitting in deep neural networks? (Select all that apply)",
                                    "options": ["A) Dropout", "B) L2 Regularization (Weight Decay)", "C) Early Stopping", "D) Data Augmentation"],
                                    "correct": ["A) Dropout", "B) L2 Regularization (Weight Decay)", "C) Early Stopping", "D) Data Augmentation"],
                                    "explanation": "All four techniques (Dropout, L2 regularization, Early stopping, and Data augmentation) are standard regularization methods used to mitigate overfitting."
                                },
                                {
                                    "id": "q3",
                                    "type": "NAT",
                                    "question": "If $A$ and $B$ are two independent events with $P(A) = 0.5$ and $P(B) = 0.2$, what is the probability $P(A \\cup B)$? (Round off to 1 decimal place, e.g. 0.6)",
                                    "correct": 0.6,
                                    "tolerance": 0.05,
                                    "explanation": "Since $A$ and $B$ are independent:\n"
                                                   "$$P(A \\cap B) = P(A) \\times P(B) = 0.5 \\times 0.2 = 0.1$$\n\n"
                                                   "Using the addition rule of probability:\n"
                                                   "$$P(A \\cup B) = P(A) + P(B) - P(A \\cap B) = 0.5 + 0.2 - 0.1 = 0.6$$"
                                },
                                {
                                    "id": "q4",
                                    "type": "MCQ",
                                    "question": "What is the primary objective of Principal Component Analysis (PCA)?",
                                    "options": ["A) To maximize class separation.", "B) To project the data onto directions of maximum variance.", "C) To predict continuous target variables.", "D) To cluster data points into $K$ groups."],
                                    "correct": "B) To project the data onto directions of maximum variance.",
                                    "explanation": "PCA is a dimensionality reduction technique that finds the principal components (orthogonal directions) along which the variance of the data is maximized."
                                },
                                {
                                    "id": "q5",
                                    "type": "NAT",
                                    "question": "Find the derivative of the function $f(x) = 3x^2 + 5x$ at $x = 4$. (Enter your answer as a single integer/decimal)",
                                    "correct": 29.0,
                                    "tolerance": 0,
                                    "explanation": "Calculate the first derivative:\n"
                                                   "$$f'(x) = 6x + 5$$\n\n"
                                                   "Substitute $x = 4$:\n"
                                                   "$$f'(4) = 6(4) + 5 = 24 + 5 = 29.0$$"
                                }
                            ]
                            
                        col_pad, col_exam_area = st.columns([0.15, 3.85])
                        with col_exam_area:
                            with st.expander(f"📝 Attempt {day['title']} (Interactive Exam)", expanded=False):
                                # Initial state tracking
                                if "exam_answers" not in st.session_state:
                                    st.session_state.exam_answers = {}
                                if "exam_submitted" not in st.session_state:
                                    st.session_state.exam_submitted = {}
                                    
                                submitted_this_exam = st.session_state.exam_submitted.get(exam_id, False)
                                
                                # Reset button
                                if submitted_this_exam:
                                    if st.button("🔄 Retake This Exam", key=f"retake_btn_{day_id}"):
                                        st.session_state.exam_submitted[exam_id] = False
                                        if exam_id in st.session_state.exam_answers:
                                            st.session_state.exam_answers[exam_id] = {}
                                        st.rerun()
                                
                                st.markdown("---")
                                
                                # Rendering questions
                                user_answers = st.session_state.exam_answers.setdefault(exam_id, {})
                                
                                for q_idx, q in enumerate(INLINE_QUESTIONS):
                                    q_id = q["id"]
                                    st.markdown(f"**Q{q_idx+1} ({q['type']}):**")
                                    st.markdown(q["question"])
                                    
                                    if not submitted_this_exam:
                                        if q["type"] == "MCQ":
                                            user_answers[q_id] = st.radio("Choose option:", q["options"], index=None, key=f"inline_mcq_{day_id}_{q_id}")
                                        elif q["type"] == "MSQ":
                                            selected_opts = []
                                            for opt in q["options"]:
                                                if st.checkbox(opt, key=f"inline_msq_{day_id}_{q_id}_{opt}"):
                                                    selected_opts.append(opt)
                                            user_answers[q_id] = selected_opts
                                        elif q["type"] == "NAT":
                                            user_answers[q_id] = st.number_input("Enter numerical value:", value=None, format="%.4f", placeholder="e.g. 0.36", key=f"inline_nat_{day_id}_{q_id}")
                                    else:
                                        # Submitted view: display chosen answer and correctness
                                        chosen = user_answers.get(q_id, None)
                                        correct = q["correct"]
                                        
                                        if q["type"] == "MCQ":
                                            st.markdown(f"**Your Answer:** {chosen if chosen else 'Not attempted'}")
                                            if chosen == correct:
                                                st.success("✅ Correct! (+2 Marks)")
                                            else:
                                                st.error(f"❌ Incorrect. Correct Answer: {correct} (-0.66 Negative Marking)")
                                        elif q["type"] == "MSQ":
                                            st.markdown(f"**Your Answer:** {', '.join(chosen) if chosen else 'Not attempted'}")
                                            if set(chosen or []) == set(correct):
                                                st.success("✅ Correct! (+2 Marks)")
                                            else:
                                                st.error(f"❌ Incorrect. Correct Answer: {', '.join(correct)}")
                                        elif q["type"] == "NAT":
                                            st.markdown(f"**Your Answer:** {chosen if chosen is not None else 'Not attempted'}")
                                            is_correct = False
                                            if chosen is not None:
                                                try:
                                                    is_correct = abs(float(chosen) - float(correct)) <= q["tolerance"]
                                                except:
                                                    pass
                                            if is_correct:
                                                st.success(f"✅ Correct! (+2 Marks)")
                                            else:
                                                st.error(f"❌ Incorrect. Correct Answer: {correct}")
                                                
                                        with st.expander("📚 View Solved Explanation"):
                                            st.markdown(q["explanation"])
                                    
                                    st.markdown("<hr style='margin:10px 0; border:0; border-top:1px dashed rgba(255,255,255,0.04);'>", unsafe_allow_html=True)
                                    
                                # Submit handle
                                if not submitted_this_exam:
                                    if st.button("🚀 Submit Premium Exam Paper", type="primary", key=f"submit_inline_{day_id}"):
                                        st.session_state.exam_submitted[exam_id] = True
                                        
                                        # Calculate Score
                                        raw_score = 0.0
                                        correct_count = 0
                                        attempted_count = 0
                                        
                                        for q in INLINE_QUESTIONS:
                                            q_id = q["id"]
                                            chosen = user_answers.get(q_id, None)
                                            correct = q["correct"]
                                            
                                            if q["type"] == "MCQ":
                                                if chosen:
                                                    attempted_count += 1
                                                    if chosen == correct:
                                                        raw_score += 2.0
                                                        correct_count += 1
                                                    else:
                                                        raw_score -= 0.66
                                            elif q["type"] == "MSQ":
                                                if chosen:
                                                    attempted_count += 1
                                                    if set(chosen) == set(correct):
                                                        raw_score += 2.0
                                                        correct_count += 1
                                            elif q["type"] == "NAT":
                                                if chosen is not None:
                                                    attempted_count += 1
                                                    is_correct = False
                                                    try:
                                                        is_correct = abs(float(chosen) - float(correct)) <= q["tolerance"]
                                                    except:
                                                        pass
                                                    if is_correct:
                                                        raw_score += 2.0
                                                        correct_count += 1
                                                        
                                        st.session_state[f"score_{exam_id}"] = round(raw_score, 2)
                                        st.session_state[f"acc_{exam_id}"] = round((correct_count / attempted_count * 100), 1) if attempted_count > 0 else 0.0
                                        st.session_state[f"correct_{exam_id}"] = correct_count
                                        st.session_state[f"attempted_{exam_id}"] = attempted_count
                                        
                                        st.balloons()
                                        st.rerun()
                                else:
                                    # Show results summary
                                    score = st.session_state.get(f"score_{exam_id}", 0.0)
                                    accuracy = st.session_state.get(f"acc_{exam_id}", 0.0)
                                    correct_c = st.session_state.get(f"correct_{exam_id}", 0)
                                    attempted_c = st.session_state.get(f"attempted_{exam_id}", 0)
                                    
                                    st.markdown("##### 📊 Test Performance Summary")
                                    col_m1, col_m2 = st.columns(2)
                                    with col_m1:
                                        st.metric("Total Score", f"{score} / 10", "Marks Scored")
                                    with col_m2:
                                        st.metric("Accuracy Rate", f"{accuracy}%", f"{correct_c}/{attempted_c} Correct")
                                        
                                    # Option to log directly to logbook
                                    log_key_str = f"logged_{exam_id}_{score}"
                                    if log_key_str not in st.session_state:
                                        if st.button("➕ Log this score to my Log Book", key=f"log_inline_{day_id}"):
                                            new_mock = {
                                                "id": str(int(pd.Timestamp.now().timestamp() * 1000)),
                                                "name": exam_name,
                                                "score": float(score) * 10.0, # Scale to out of 100
                                                "accuracy": float(accuracy),
                                                "date": date.today().strftime("%Y-%m-%d"),
                                                "type": "Full Length Mock"
                                            }
                                            state["mocks"].append(new_mock)
                                            state["mocks"].sort(key=lambda x: x["date"])
                                            commit_changes()
                                            st.session_state[log_key_str] = True
                                            st.success("Entry successfully logged in your Mock Attempts Log Book!")
                                            st.rerun()
                                    else:
                                        st.info("✓ Score successfully saved to your Log Book.")



                st.markdown("<hr style='margin:10px 0; border:0; border-top:1px solid rgba(255,255,255,0.04);'>", unsafe_allow_html=True)

# ------------------------------------------
# Tab 2: Syllabus Tracker
# ------------------------------------------
with tabs[2]:
    st.subheader("Official GATE Data Science & AI Syllabus")
    st.caption("Verify you have covered every specific sub-topic listed in the official syllabus handbook.")
    
    col_syll1, col_syll2 = st.columns(2)
    
    # Split subjects between two columns
    sections_list = list(SYLLABUS_SECTIONS.keys())
    
    with col_syll1:
        for subject in sections_list[:4]:
            st.markdown(f"#### {subject}")
            for code, name in SYLLABUS_SECTIONS[subject]:
                checked = st.checkbox(name, value=(code in state["syllabus_checked"]), key=f"syll_{code}")
                if checked != (code in state["syllabus_checked"]):
                    if checked:
                        state["syllabus_checked"].append(code)
                    else:
                        state["syllabus_checked"] = [c for c in state["syllabus_checked"] if c != code]
                    commit_changes()
                    st.rerun()
            st.markdown("---")
            
    with col_syll2:
        for subject in sections_list[4:]:
            st.markdown(f"#### {subject}")
            for code, name in SYLLABUS_SECTIONS[subject]:
                checked = st.checkbox(name, value=(code in state["syllabus_checked"]), key=f"syll_{code}")
                if checked != (code in state["syllabus_checked"]):
                    if checked:
                        state["syllabus_checked"].append(code)
                    else:
                        state["syllabus_checked"] = [c for c in state["syllabus_checked"] if c != code]
                    commit_changes()
                    st.rerun()
            st.markdown("---")

# ------------------------------------------
# Tab 3: Free Resources
# ------------------------------------------
with tabs[3]:
    st.subheader("Curated Free Online Materials")
    st.caption("These resources are highly recommended by toppers to master theoretical concepts and practice problems.")
    
    # Filter Toolbar
    col_search, col_tag = st.columns([2, 1])
    with col_search:
        search_query = st.text_input("Search catalog by keyword:", placeholder="e.g. Gilbert Strang, DBMS, NPTEL")
    
    with col_tag:
        cat_filter = st.selectbox("Category Filter:", ["All", "Mathematics & Stats", "Computer Science & DBMS", "ML & AI"])
        
    category_map = {"All": "all", "Mathematics & Stats": "math", "Computer Science & DBMS": "cs", "ML & AI": "ml-ai"}
    selected_cat = category_map[cat_filter]
    
    # Filter database
    res_list = []
    for res in RESOURCES_CATALOG:
        # Category Filter
        if selected_cat != "all" and res["category"] != selected_cat:
            continue
        # Search text
        if search_query:
            q = search_query.lower()
            if q not in res["name"].lower() and q not in res["type"].lower():
                continue
        res_list.append(res)
        
    if not res_list:
        st.warning("No resources match your search filters.")
    else:
        # Build Pandas DataFrame to display beautifully
        df = pd.DataFrame(res_list)
        # Beautify display columns
        df.columns = ["Category Key", "Resource Name", "Format / Type", "Link URL"]
        df["Category Key"] = df["Category Key"].replace({"math": "Math & Stats", "cs": "CS & DBMS", "ml-ai": "ML & AI"})
        
        st.dataframe(df, use_container_width=True, column_config={
            "Link URL": st.column_config.LinkColumn("Access Resource")
        })

# ------------------------------------------
# Tab 4: Mock Tests Log
# ------------------------------------------
with tabs[4]:
    st.subheader("GATE DA Mock Center")
    
    # Mode selection
    is_unlocked = state.get("is_premium_unlocked", False)
    mode_options = ["📊 Mock Attempt Log Book", "🏆 Premium Practice Mock Center" + (" (Locked 🔒)" if not is_unlocked else " (Unlocked)")]
    mock_mode = st.radio("Choose Section:", mode_options, horizontal=True, key="mock_center_mode_select")
    
    if "Log Book" in mock_mode:
        col_form, col_chart = st.columns([1, 1.5])
        
        with col_form:
            st.markdown("#### Log New Attempt")
            
            with st.form("new_mock_form", clear_on_submit=True):
                m_name = st.text_input("Mock Test Name", placeholder="e.g. GATE DA 2024 PYQ Paper, MadeEasy Mock 5")
                m_score = st.number_input("Marks Scored (out of 100)", min_value=0.0, max_value=100.0, step=0.25, value=50.0)
                m_accuracy = st.number_input("Accuracy Rate % (optional)", min_value=0.0, max_value=100.0, step=0.1, value=75.0)
                m_date = st.date_input("Attempt Date", value=date.today())
                m_type = st.selectbox("Mock Type", ["Full Length Mock", "Subject Test", "Official PYQ Paper"])
                
                submitted = st.form_submit_button("Save Mock Entry")
                if submitted:
                    if not m_name:
                        st.error("Please enter a valid mock name.")
                    else:
                        new_mock = {
                            "id": str(int(pd.Timestamp.now().timestamp() * 1000)),
                            "name": m_name,
                            "score": m_score,
                            "accuracy": m_accuracy,
                            "date": m_date.strftime("%Y-%m-%d"),
                            "type": m_type
                        }
                        state["mocks"].append(new_mock)
                        # Sort mocks by date
                        state["mocks"].sort(key=lambda x: x["date"])
                        commit_changes()
                        st.success("Mock test saved successfully!")
                        st.rerun()
                        
        with col_chart:
            st.markdown("#### Score Progression Chart")
            if not state["mocks"]:
                st.info("No mock test entries logged yet. Add one to view progress graph.")
            else:
                # Map mock scores to dataframe
                mock_df = pd.DataFrame(state["mocks"])
                mock_df["date"] = pd.to_datetime(mock_df["date"])
                
                # Simple line chart
                st.line_chart(mock_df.set_index("name")["score"])
                
        # Display table list
        st.markdown("#### Attempt History")
        if not state["mocks"]:
            st.write("No attempts logged.")
        else:
            history_df = pd.DataFrame(state["mocks"])[::-1] # Reverse for newest first
            # Format columns
            history_df = history_df[["date", "name", "type", "score", "accuracy", "id"]]
            history_df.columns = ["Attempt Date", "Test Name", "Type", "Marks /100", "Accuracy %", "ID"]
            
            st.dataframe(history_df, use_container_width=True)
            
            # Delete row handle
            to_delete = st.selectbox("Select a mock ID to remove:", ["None"] + list(history_df["ID"].values))
            if to_delete != "None":
                if st.button("Delete Selected Mock"):
                    state["mocks"] = [m for m in state["mocks"] if m["id"] != to_delete]
                    commit_changes()
                    st.success("Mock test entry deleted!")
                    st.rerun()
                    
    else:
        # Premium Practice Mock Center
        if not is_unlocked:
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(255, 126, 95, 0.1) 0%, rgba(254, 180, 123, 0.1) 100%); 
                        border: 1px solid rgba(255, 126, 95, 0.25); border-radius: 12px; padding: 24px; text-align: center; margin-bottom: 20px;">
                <h3 style='margin:0; font-weight:800; color: #ff7e5f; font-family: "Outfit", sans-serif;'>🔒 Premium GATE DA Mock Test Pack</h3>
                <p style='margin: 10px 0; color: #8c9bb4; font-size:14px;'>
                    Gain access to exclusive full-length mock exams custom-built by top educators. Features interactive testing, automatic grading, and detailed explanations.
                </p>
                <div style='font-size: 28px; font-weight: 800; color: #ff7e5f; margin: 15px 0;'>₹10 <span style='font-size:14px; font-weight:normal; color:#8c9bb4;'>one-time payment</span></div>
            </div>
            """, unsafe_allow_html=True)
            
            col_pay_info, col_pay_qr = st.columns([1.2, 1])
            with col_pay_info:
                st.markdown("#### 💎 Features Included:")
                st.markdown("""
                *   **2 Full-Length Mock Exams** containing high-yield GATE-DA questions.
                *   **MCQ, MSQ, and NAT** formats designed to match IIT-Roorkee & IISc levels.
                *   **Live grading** with score calculation, accuracy tracking, and streak logging.
                *   **Step-by-Step solutions** with LaTeX mathematical proofs for every single question.
                """)
                
                show_qr = st.toggle("👉 Click to Open Payment QR Code", key="toggle_show_qr")
                
            with col_pay_qr:
                if show_qr:
                    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
                    # Display the generated QR code image
                    st.image("upi_qr.png", caption="Scan using GPay, PhonePe, Paytm or any UPI App to Pay ₹10", width=220)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.success("UPI ID: 6376541591@fam")
                    
                    utr_input = st.text_input("Enter 12-digit UPI Ref/UTR No. after payment:", placeholder="e.g. 620584739201", key="confirm_pay_utr")
                    if st.button("🚀 Verify & Unlock", type="primary", key="confirm_pay_btn"):
                        if not utr_input:
                            st.error("Please enter the 12-digit UTR/Ref No.")
                        elif len(utr_input) != 12 or not utr_input.isdigit():
                            st.error("Invalid UTR. The UPI Ref No. must be exactly 12 numeric digits.")
                        else:
                            import time
                            with st.spinner("Connecting to UPI networks to verify transaction..."):
                                time.sleep(2)
                            state["is_premium_unlocked"] = True
                            commit_changes()
                            st.balloons()
                            st.success("🎉 Payment Verified! Premium Mock Center is now unlocked!")
                            st.rerun()
                        
        else:
            # Unlocked Premium Center
            st.markdown("### 🏆 Practice Exam Center")
            st.caption("Select a custom mock exam to attempt. Solve the questions under exam conditions.")
            
            # Static mock data definition
            MOCK_EXAMS_DATA = [
                {
                    "id": "premium_mock_1",
                    "name": "Mock Exam 1: GATE DA Full-Length Prediction Mock",
                    "questions": [
                        {
                            "id": "q1",
                            "type": "MCQ",
                            "question": "Let $A$ be a $3 \\times 3$ matrix with eigenvalues $1, 2, 3$. What is the determinant of the matrix $B = A^2 - A$?",
                            "options": ["A) 0", "B) 6", "C) 12", "D) 18"],
                            "correct": "A) 0",
                            "explanation": "The eigenvalues of $A$ are $\\lambda_1 = 1$, $\\lambda_2 = 2$, and $\\lambda_3 = 3$.\n\n"
                                           "The eigenvalues of the matrix $B = A^2 - A$ are given by $f(\\lambda_i) = \\lambda_i^2 - \\lambda_i$:\n"
                                           "- For $\\lambda_1 = 1$: $1^2 - 1 = 0$\n"
                                           "- For $\\lambda_2 = 2$: $2^2 - 2 = 2$\n"
                                           "- For $\\lambda_3 = 3$: $3^2 - 3 = 6$\n\n"
                                           "The determinant of a matrix is the product of its eigenvalues. Therefore, $\\text{det}(B) = 0 \\times 2 \\times 6 = 0$. Thus, Option A is correct."
                        },
                        {
                            "id": "q2",
                            "type": "MSQ",
                            "question": "Which of the following statements are **TRUE** regarding Artificial Intelligence search algorithms? (Select all that apply)",
                            "options": [
                                "A) A* search is optimal if the heuristic function $h(n)$ is admissible for tree search.",
                                "B) Uniform Cost Search (UCS) is optimal and complete if step costs are strictly positive.",
                                "C) A consistent heuristic is always admissible.",
                                "D) Depth-First Search (DFS) has a worst-case space complexity of $O(b^d)$ where $b$ is the branching factor and $d$ is the depth."
                            ],
                            "correct": ["A) A* search is optimal if the heuristic function $h(n)$ is admissible for tree search.", 
                                        "B) Uniform Cost Search (UCS) is optimal and complete if step costs are strictly positive.", 
                                        "C) A consistent heuristic is always admissible."],
                            "explanation": "Let's analyze the statements:\n"
                                           "- **A is TRUE**: Admissibility of $h(n)$ guarantees optimality in tree search.\n"
                                           "- **B is TRUE**: UCS is a special case of Dijkstra's algorithm; it is complete and optimal if step costs $\\ge \\epsilon > 0$.\n"
                                           "- **C is TRUE**: Consistency ($h(n) \\le c(n, a, n') + h(n')$) is a stronger condition than admissibility; all consistent heuristics are admissible.\n"
                                           "- **D is FALSE**: DFS has a space complexity of $O(bd)$ in the worst case, not $O(b^d)$. (BFS has $O(b^d)$ space complexity)."
                        },
                        {
                            "id": "q3",
                            "type": "NAT",
                            "question": "Consider a Naive Bayes classifier with two classes $C_1$ and $C_2$. The prior probability is $P(C_1) = 0.6$. "
                                        "For a binary feature $X$, the conditional probabilities are $P(X=1 \\mid C_1) = 0.3$ and $P(X=1 \\mid C_2) = 0.8$. "
                                        "Compute the posterior probability $P(C_1 \\mid X=1)$. (Enter your answer rounded off to 2 decimal places, e.g. 0.36)",
                            "correct": 0.36,
                            "tolerance": 0.01,
                            "explanation": "By Bayes' Theorem:\n"
                                           "$$P(C_1 \\mid X=1) = \\frac{P(X=1 \\mid C_1) P(C_1)}{P(X=1)}$$\n\n"
                                           "First, calculate the marginal probability $P(X=1)$ using the law of total probability:\n"
                                           "$$P(X=1) = P(X=1 \\mid C_1)P(C_1) + P(X=1 \\mid C_2)P(C_2)$$\n"
                                           "Given $P(C_1) = 0.6 \\implies P(C_2) = 1 - 0.6 = 0.4$:\n"
                                           "$$P(X=1) = (0.3 \\times 0.6) + (0.8 \\times 0.4) = 0.18 + 0.32 = 0.50$$\n\n"
                                           "Now, substitute back into Bayes' formula:\n"
                                           "$$P(C_1 \\mid X=1) = \\frac{0.18}{0.50} = 0.36$$"
                        },
                        {
                            "id": "q4",
                            "type": "MCQ",
                            "question": "Let $R(A, B, C, D, E)$ be a relational schema with functional dependencies: $A \\to B$, $B \\to C$, and $D \\to E$. "
                                        "Which of the following is the candidate key for $R$?",
                            "options": ["A) A", "B) AD", "C) ADE", "D) ABD"],
                            "correct": "B) AD",
                            "explanation": "To find the candidate key, we compute the closure of attributes:\n"
                                           "- $\\{A\\}^+ = \\{A, B, C\\}$ (does not contain $D, E$)\n"
                                           "- $\\{AD\\}^+ = \\{A, D\\}^+$\n"
                                           "  Using $A \\to B$: $\\{A, D, B\\}$\n"
                                           "  Using $B \\to C$: $\\{A, D, B, C\\}$\n"
                                           "  Using $D \\to E$: $\\{A, D, B, C, E\\}$ = all attributes of relation $R$.\n\n"
                                           "Since $\\{AD\\}^+$ contains all attributes and no proper subset of $\\{AD\\}$ is a superkey, $AD$ is the candidate key."
                        },
                        {
                            "id": "q5",
                            "type": "NAT",
                            "question": "The probability density function of a continuous random variable $X$ is given by $f(x) = k x^2$ for $0 \\le x \\le 2$, and $f(x) = 0$ otherwise. "
                                        "Calculate the value of the constant $k$. (Enter your answer as a decimal rounded off to 3 decimal places, e.g. 0.375)",
                            "correct": 0.375,
                            "tolerance": 0.005,
                            "explanation": "Since $f(x)$ is a probability density function, the total area under the curve must equal 1:\n"
                                           "$$\\int_{-\\infty}^{\\infty} f(x) dx = 1 \\implies \\int_0^2 k x^2 dx = 1$$\n\n"
                                           "Perform the integration:\n"
                                           "$$k \\left[ \\frac{x^3}{3} \\right]_0^2 = 1 \\implies k \\left( \\frac{8}{3} - 0 \\right) = 1$$\n"
                                           "$$k \\frac{8}{3} = 1 \\implies k = \\frac{3}{8} = 0.375$$"
                        }
                    ]
                },
                {
                    "id": "premium_mock_2",
                    "name": "Mock Exam 2: Advanced AI, ML & Math Subject Mock",
                    "questions": [
                        {
                            "id": "q1",
                            "type": "MCQ",
                            "question": "Let $X$ and $Y$ be independent Poisson random variables with parameters $\\lambda_1 = 2$ and $\\lambda_2 = 3$ respectively. "
                                        "What is the probability $P(X + Y = 1)$?",
                            "options": ["A) $e^{-5}$", "B) $5e^{-5}$", "C) $6e^{-5}$", "D) $2.5e^{-5}$"],
                            "correct": "B) $5e^{-5}$",
                            "explanation": "Since $X$ and $Y$ are independent Poisson random variables with parameters $\\lambda_1$ and $\\lambda_2$, their sum $Z = X + Y$ is also a Poisson random variable with parameter $\\lambda = \\lambda_1 + \\lambda_2 = 2 + 3 = 5$.\n\n"
                                           "The probability mass function of a Poisson random variable is $P(Z = z) = \\frac{e^{-\\lambda} \\lambda^z}{z!}.\n\n"
                                           "For $z = 1$:\n"
                                           "$$P(X + Y = 1) = \\frac{e^{-5} 5^1}{1!} = 5e^{-5}$$"
                        },
                        {
                            "id": "q2",
                            "type": "MSQ",
                            "question": "Which of the following are **TRUE** regarding support vector machines (SVM)? (Select all that apply)",
                            "options": [
                                "A) In a soft-margin SVM, the parameter $C$ controls the trade-off between margin size and classification errors.",
                                "B) If we increase $C$, the margin size decreases and the classifier becomes more prone to overfitting.",
                                "C) The dual formulation of SVM optimization depends only on the dot products of input feature vectors.",
                                "D) The radial basis function (RBF) kernel maps the inputs to a finite-dimensional feature space."
                            ],
                            "correct": ["A) In a soft-margin SVM, the parameter $C$ controls the trade-off between margin size and classification errors.",
                                        "B) If we increase $C$, the margin size decreases and the classifier becomes more prone to overfitting.",
                                        "C) The dual formulation of SVM optimization depends only on the dot products of input feature vectors."],
                            "explanation": "- **A is TRUE**: $C$ regulates regularization. High $C$ prioritizes correct classification, small $C$ prioritizes a wider margin.\n"
                                           "- **B is TRUE**: High $C$ fits training data very strictly, shrinking the margin, leading to overfitting risk.\n"
                                           "- **C is TRUE**: The dual objective function involves $\\sum \\alpha_i \\alpha_j y_i y_j (x_i \\cdot x_j)$, enabling the kernel trick.\n"
                                           "- **D is FALSE**: The RBF kernel maps inputs to an *infinite*-dimensional feature space, not finite."
                        },
                        {
                            "id": "q3",
                            "type": "NAT",
                            "question": "Assume we run the K-Means algorithm on a 1D dataset containing points $\\{2, 4, 10, 12, 20\\}$ with $K = 2$. "
                                        "The initial centroids are chosen as $c_1 = 3$ and $c_2 = 15$. "
                                        "What is the value of the updated centroid $c_1$ after the first iteration? (Enter your answer as a single integer/decimal)",
                            "correct": 3.0,
                            "tolerance": 0.01,
                            "explanation": "Let's run the first assignment step:\n"
                                           "- Point 2: distance to $c_1(3)$ is 1, distance to $c_2(15)$ is 13. Assign to Cluster 1.\n"
                                           "- Point 4: distance to $c_1(3)$ is 1, distance to $c_2(15)$ is 11. Assign to Cluster 1.\n"
                                           "- Point 10: distance to $c_1(3)$ is 7, distance to $c_2(15)$ is 5. Assign to Cluster 2.\n"
                                           "- Point 12: distance to $c_1(3)$ is 9, distance to $c_2(15)$ is 3. Assign to Cluster 2.\n"
                                           "- Point 20: distance to $c_1(3)$ is 17, distance to $c_2(15)$ is 5. Assign to Cluster 2.\n\n"
                                           "Cluster 1 points: $\\{2, 4\\}$.\n"
                                           "Cluster 2 points: $\\{10, 12, 20\\}$.\n\n"
                                           "Updated centroid $c_1 = \\frac{2 + 4}{2} = 3.0$."
                        },
                        {
                            "id": "q4",
                            "type": "MCQ",
                            "question": "Let $X$ be a random variable representing the height of students. We collect a sample of size $n = 100$ "
                                        "and calculate the sample mean $\\bar{x} = 170$ cm with sample standard deviation $s = 10$ cm. "
                                        "What is the approximate $95\\%$ confidence interval for the population mean? (Use $z_{0.025} = 1.96$)",
                            "options": ["A) [169.02, 170.98]", "B) [168.04, 171.96]", "C) [165.02, 174.98]", "D) [167.08, 172.92]"],
                            "correct": "B) [168.04, 171.96]",
                            "explanation": "The formula for the confidence interval of the mean is:\n"
                                           "$$\\bar{x} \\pm z \\frac{s}{\\sqrt{n}}$$\n\n"
                                           "Substitute the given values:\n"
                                           "- $\\bar{x} = 170$\n"
                                           "- $z = 1.96$\n"
                                           "- $s = 10$\n"
                                           "- $n = 100 \\implies \\sqrt{n} = 10$\n\n"
                                           "Calculate standard error:\n"
                                           "$$\\text{SE} = \\frac{10}{10} = 1$$\n\n"
                                           "Calculate margin of error:\n"
                                           "$$\\text{ME} = 1.96 \\times 1 = 1.96$$\n\n"
                                           "Thus, the interval is:\n"
                                           "$$[170 - 1.96, 170 + 1.96] = [168.04, 171.96]$$"
                        },
                        {
                            "id": "q5",
                            "type": "NAT",
                            "question": "Find the maximum value of the function $f(x) = -2x^2 + 8x + 5$ using optimization methods. "
                                        "(Enter your answer as a single integer/decimal)",
                            "correct": 13.0,
                            "tolerance": 0.01,
                            "explanation": "To find the maximum, we calculate the first derivative and set it to zero:\n"
                                           "$$f'(x) = -4x + 8 = 0 \\implies x = 2$$\n\n"
                                           "Verify using the second derivative:\n"
                                           "$$f''(x) = -4 < 0$$\n"
                                           "Since the second derivative is negative, $x=2$ is a local and global maximum.\n\n"
                                           "Substitute $x=2$ back into the original function $f(x)$:\n"
                                           "$$f(2) = -2(2)^2 + 8(2) + 5 = -8 + 16 + 5 = 13.0$$"
                        }
                    ]
                }
            ]
            
            selected_exam_id = st.selectbox("Select Premium Exam Paper:", [e["name"] for e in MOCK_EXAMS_DATA])
            exam = [e for e in MOCK_EXAMS_DATA if e["name"] == selected_exam_id][0]
            
            # Initial state tracking
            if "exam_answers" not in st.session_state:
                st.session_state.exam_answers = {}
            if "exam_submitted" not in st.session_state:
                st.session_state.exam_submitted = {}
                
            exam_id = exam["id"]
            submitted_this_exam = st.session_state.exam_submitted.get(exam_id, False)
            
            # Reset button
            if submitted_this_exam:
                if st.button("🔄 Retake This Exam"):
                    st.session_state.exam_submitted[exam_id] = False
                    if exam_id in st.session_state.exam_answers:
                        st.session_state.exam_answers[exam_id] = {}
                    st.rerun()
            
            st.markdown("---")
            
            # Rendering questions
            user_answers = st.session_state.exam_answers.setdefault(exam_id, {})
            
            for idx, q in enumerate(exam["questions"]):
                q_id = q["id"]
                st.markdown(f"#### Q{idx+1} ({q['type']}):")
                st.markdown(q["question"])
                
                if not submitted_this_exam:
                    if q["type"] == "MCQ":
                        user_answers[q_id] = st.radio("Choose option:", q["options"], index=None, key=f"p_mcq_{exam_id}_{q_id}")
                    elif q["type"] == "MSQ":
                        selected_opts = []
                        for opt in q["options"]:
                            if st.checkbox(opt, key=f"p_msq_{exam_id}_{q_id}_{opt}"):
                                selected_opts.append(opt)
                        user_answers[q_id] = selected_opts
                    elif q["type"] == "NAT":
                        user_answers[q_id] = st.number_input("Enter numerical value:", value=None, format="%.4f", placeholder="e.g. 0.36", key=f"p_nat_{exam_id}_{q_id}")
                else:
                    # Submitted view: display chosen answer and correctness
                    chosen = user_answers.get(q_id, None)
                    correct = q["correct"]
                    
                    if q["type"] == "MCQ":
                        st.markdown(f"**Your Answer:** {chosen if chosen else 'Not attempted'}")
                        if chosen == correct:
                            st.success("✅ Correct! (+2 Marks)")
                        else:
                            st.error(f"❌ Incorrect. Correct Answer: {correct} (-0.66 Negative Marking)")
                    elif q["type"] == "MSQ":
                        st.markdown(f"**Your Answer:** {', '.join(chosen) if chosen else 'Not attempted'}")
                        # Check equality of sets
                        if set(chosen or []) == set(correct):
                            st.success("✅ Correct! (+2 Marks)")
                        else:
                            st.error(f"❌ Incorrect. Correct Answer: {', '.join(correct)}")
                    elif q["type"] == "NAT":
                        st.markdown(f"**Your Answer:** {chosen if chosen is not None else 'Not attempted'}")
                        # Check tolerance
                        is_correct = False
                        if chosen is not None:
                            try:
                                is_correct = abs(float(chosen) - float(correct)) <= q["tolerance"]
                            except:
                                pass
                        if is_correct:
                            st.success(f"✅ Correct! (+2 Marks)")
                        else:
                            st.error(f"❌ Incorrect. Correct Answer: {correct}")
                            
                    with st.expander("📚 View Solved Explanation"):
                        st.markdown(q["explanation"])
                
                st.markdown("<hr style='margin:15px 0; border:0; border-top:1px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
                
            # Submit handle
            if not submitted_this_exam:
                if st.button("🚀 Submit Premium Exam Paper", type="primary"):
                    st.session_state.exam_submitted[exam_id] = True
                    
                    # Calculate Score
                    raw_score = 0.0
                    correct_count = 0
                    attempted_count = 0
                    
                    for q in exam["questions"]:
                        q_id = q["id"]
                        chosen = user_answers.get(q_id, None)
                        correct = q["correct"]
                        
                        if q["type"] == "MCQ":
                            if chosen:
                                attempted_count += 1
                                if chosen == correct:
                                    raw_score += 2.0
                                    correct_count += 1
                                else:
                                    raw_score -= 0.66
                        elif q["type"] == "MSQ":
                            if chosen:
                                attempted_count += 1
                                if set(chosen) == set(correct):
                                    raw_score += 2.0
                                    correct_count += 1
                        elif q["type"] == "NAT":
                            if chosen is not None:
                                attempted_count += 1
                                is_correct = False
                                try:
                                    is_correct = abs(float(chosen) - float(correct)) <= q["tolerance"]
                                except:
                                    pass
                                if is_correct:
                                    raw_score += 2.0
                                    correct_count += 1
                                    
                    st.session_state[f"score_{exam_id}"] = round(raw_score, 2)
                    st.session_state[f"acc_{exam_id}"] = round((correct_count / attempted_count * 100), 1) if attempted_count > 0 else 0.0
                    st.session_state[f"correct_{exam_id}"] = correct_count
                    st.session_state[f"attempted_{exam_id}"] = attempted_count
                    
                    st.balloons()
                    st.rerun()
            else:
                # Show results summary
                score = st.session_state.get(f"score_{exam_id}", 0.0)
                accuracy = st.session_state.get(f"acc_{exam_id}", 0.0)
                correct_c = st.session_state.get(f"correct_{exam_id}", 0)
                attempted_c = st.session_state.get(f"attempted_{exam_id}", 0)
                
                st.markdown("### 📊 Test Performance Summary")
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("Total Score", f"{score} / 10", "Marks Scored")
                with col_m2:
                    st.metric("Accuracy Rate", f"{accuracy}%", f"{correct_c} Correct")
                with col_m3:
                    st.metric("Questions Attempted", f"{attempted_c} / 5", "Total Questions")
                    
                # Option to log directly to logbook
                log_key_str = f"logged_{exam_id}_{score}"
                if log_key_str not in st.session_state:
                    if st.button("➕ Log this score to my Log Book"):
                        new_mock = {
                            "id": str(int(pd.Timestamp.now().timestamp() * 1000)),
                            "name": exam["name"],
                            "score": float(score) * 10.0, # Scale to out of 100
                            "accuracy": float(accuracy),
                            "date": date.today().strftime("%Y-%m-%d"),
                            "type": "Full Length Mock"
                        }
                        state["mocks"].append(new_mock)
                        state["mocks"].sort(key=lambda x: x["date"])
                        commit_changes()
                        st.session_state[log_key_str] = True
                        st.success("Entry successfully logged in your Mock Attempts Log Book!")
                        st.rerun()
                else:
                    st.info("✓ Score successfully saved to your Log Book.")


# ------------------------------------------
# Tab 5: Performance Analytics
# ------------------------------------------
with tabs[0]:
    st.subheader("Performance Insights & Review Notes")
    st.caption("Deep analysis based on daily study review logs.")
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Study Consistency", f"{progress_pct}%", "days ticked off")
    with col_stat2:
        st.metric("Hours Studied", f"{round(total_hours, 1)} hrs", "total logged time")
    with col_stat3:
        rate = round(total_hours / completed_count, 1) if completed_count > 0 else 0.0
        st.metric("Daily Study Rate", f"{rate} hrs/day", "average hours per completed day")
        
    st.markdown("---")
    
    col_an1, col_an2 = st.columns(2)
    
    # 1. Urgent Revisions Queue (Rating <= 2)
    with col_an1:
        st.markdown("#### 🚨 Urgent Revisions Queue")
        st.caption("Topics where self-assessed understanding rating was logged at 2 stars or lower.")
        
        revisions = []
        for day_id_str, log in state["daily_reviews"].items():
            if int(log.get("rating", 5)) <= 2:
                day_id = int(day_id_str)
                # Find day name
                topic = "Unknown"
                subj = "Unknown"
                for w in STUDY_PLAN:
                    d_obj = next((d for d in w["days"] if d["id"] == day_id), None)
                    if d_obj:
                        topic = d_obj["title"]
                        subj = w["subject"]
                        break
                revisions.append((day_id, topic, subj, log["rating"], log.get("notes", "")))
                
        if not revisions:
            st.success("All logged topics are set to stable confidence! No urgent revisions needed.")
        else:
            for d_id, topic, subj, rating, notes in sorted(revisions):
                st.error(f"**Day {d_id}**: {topic} ({subj}) — Confidence: **{rating}★**\n\n*Notes*: _{notes or 'No notes logged.'}_")
                
    # 2. Subject Confidence Bars
    with col_an2:
        st.markdown("#### 🧠 Subject Confidence Indices")
        st.caption("Average self-ratings across specific disciplines.")
        
        subjects = [
            ("Linear Algebra", 1, 28),
            ("Probability & Stats", 29, 56),
            ("Calculus & Optimization", 57, 70),
            ("Programming & DSA", 71, 84),
            ("DBMS & Warehousing", 85, 98),
            ("Machine Learning", 99, 126),
            ("Artificial Intelligence", 127, 140)
        ]
        
        conf_data = []
        for s_name, start, end in subjects:
            subj_ratings = []
            for d_id in range(start, end + 1):
                log = state["daily_reviews"].get(str(d_id))
                if log and "rating" in log:
                    subj_ratings.append(log["rating"])
            avg_r = sum(subj_ratings) / len(subj_ratings) if subj_ratings else 0.0
            conf_data.append({"Subject": s_name, "Average Rating": avg_r})
            
        if not any(d["Average Rating"] > 0 for d in conf_data):
            st.info("Log reviews inside the study planner to populate subject confidence charts.")
        else:
            conf_df = pd.DataFrame(conf_data)
            st.bar_chart(conf_df.set_index("Subject"))

    st.markdown("---")
    
    # 3. 180-Day Grid Calendar Matrix (HTML rendering)
    st.markdown("#### 📅 180-Day Study Calendar Matrix")
    st.caption("Green represents high confidence (4-5★), Orange represents medium (3★), and Pink represents low confidence (1-2★). Gray cells are unstudied.")
    
    grid_html = "<div class='matrix-grid'>"
    for day_id in range(1, 181):
        log = state["daily_reviews"].get(str(day_id))
        cls = "cell-empty"
        tooltip = f"Day {day_id}: Not Studied"
        
        if log:
            rating = log.get("rating", 5)
            hours = log.get("hours", 0)
            notes = log.get("notes", "").replace("'", "")
            tooltip = f"Day {day_id}: {rating}/5 stars | Hours: {hours}h | Notes: {notes[:40]}..."
            if rating <= 2: cls = "cell-low"
            elif rating == 3: cls = "cell-medium"
            else: cls = "cell-high"
        elif day_id in state["completed_days"]:
            cls = "cell-medium"
            tooltip = f"Day {day_id}: Completed (no log detail)"
            
        grid_html += f"<div class='matrix-cell {cls}' title='{tooltip}'></div>"
        
    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)

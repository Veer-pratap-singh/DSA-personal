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
            { "id": 1, "title": "Vector Operations & Combinations", "focus": "Vectors, scalar multiplication, linear combinations, span", "resource": "MIT 18.06 Gilbert Strang - Lec 1", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
            { "id": 2, "title": "Linear Independence & Dependence", "focus": "Linearly independent vector sets, verifying dependencies", "resource": "3Blue1Brown Linear Algebra - Lec 2", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab" },
            { "id": 3, "title": "Systems of Linear Equations (Ax = b)", "focus": "Matrix representations, coefficients, augmentations", "resource": "MIT 18.06 Gilbert Strang - Lec 2", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
            { "id": 4, "title": "Gaussian Elimination & Row Echelon", "focus": "Row operations, pivots, row echelon vs reduced row echelon", "resource": "MIT 18.06 Gilbert Strang - Lec 3", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
            { "id": 5, "title": "Rank of a Matrix", "focus": "Pivot variables, rank definition, rank calculation", "resource": "MIT 18.06 Gilbert Strang - Lec 7", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
            { "id": 6, "title": "Nullity & Rank-Nullity Theorem", "focus": "Free variables, null space, rank-nullity formulation", "resource": "MIT 18.06 Gilbert Strang - Lec 8", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
            { "id": 7, "title": "Weekly Review & Practice", "focus": "Practice solving system of equations, write cheat sheet", "resource": "GO Classes Linear Algebra Problems", "url": "https://www.youtube.com/@Goclasses" }
        ]
    },
    {
        "week": 2,
        "name": "Vector Spaces & Fundamental Subspaces",
        "phase": "phase1",
        "subject": "Linear Algebra",
        "days": [
            { "id": 8, "title": "Vector Spaces & Subspaces", "focus": "Definition axioms, subspace requirements, span subspaces", "resource": "MIT 18.06 Gilbert Strang - Lec 6", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
            { "id": 9, "title": "Subspace Intersection & Sum", "focus": "Verifying if intersections or unions form subspaces", "resource": "Gilbert Strang Textbook - Chapter 3", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 10, "title": "Bases & Dimension", "focus": "Definition of basis, uniqueness, computing dimensions", "resource": "MIT 18.06 Gilbert Strang - Lec 9", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
            { "id": 11, "title": "Change of Basis Matrix", "focus": "Transformation matrix from basis B1 to B2", "resource": "3Blue1Brown Linear Algebra - Lec 13", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab" },
            { "id": 12, "title": "The Four Fundamental Subspaces", "focus": "Definitions of C(A), N(A), C(A^T), N(A^T)", "resource": "MIT 18.06 Gilbert Strang - Lec 10", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
            { "id": 13, "title": "Subspace Dimensions & Relations", "focus": "Finding dimensions of the 4 subspaces for mxn matrix", "resource": "MIT 18.06 Gilbert Strang - Lec 11", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
            { "id": 14, "title": "Bases & Subspaces Practice", "focus": "Solve past GATE questions on vectors & subspaces", "resource": "GATE DA PYQs & CS math papers", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
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
            { "id": 17, "title": "Determinants & Properties", "focus": "Determinant calculation, row ops effects, volume expansion", "resource": "MIT 18.06 Gilbert Strang - Lec 18", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
            { "id": 18, "title": "Cramer's Rule & Formula", "focus": "Solving systems via Cramer's rule, cofactor formula", "resource": "MIT 18.06 Gilbert Strang - Lec 20", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
            { "id": 19, "title": "Eigenvalues & Eigenvectors", "focus": "Characteristic equation, solving det(A - λI) = 0", "resource": "MIT 18.06 Gilbert Strang - Lec 21", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
            { "id": 20, "title": "Diagonalization & Similarity", "focus": "Symmetric matrices, algebraic vs geometric multiplicity", "resource": "MIT 18.06 Gilbert Strang - Lec 22", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
            { "id": 21, "title": "Transformation & Eigenvalue practice", "focus": "Practice solving eigenvalues from GATE CS/EC papers", "resource": "GATE CSE Online Questions", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
        ]
    },
    {
        "week": 4,
        "name": "Orthogonality & Matrix Decompositions",
        "phase": "phase1",
        "subject": "Linear Algebra",
        "days": [
            { "id": 22, "title": "Inner Product & Orthogonality", "focus": "Dot products, lengths, angles, orthogonal vector spaces", "resource": "MIT 18.06 Gilbert Strang - Lec 14", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
            { "id": 23, "title": "Orthogonal Projections", "focus": "Projection onto lines, projection matrices", "resource": "MIT 18.06 Gilbert Strang - Lec 15", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
            { "id": 24, "title": "Gram-Schmidt & QR Decomposition", "focus": "Orthonormal basis construction, A = QR breakdown", "resource": "MIT 18.06 Gilbert Strang - Lec 17", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
            { "id": 25, "title": "LU Decomposition", "focus": "Lower-Upper matrix decomposition, forwards-back substitution", "resource": "MIT 18.06 Gilbert Strang - Lec 4", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
            { "id": 26, "title": "Singular Value Decomposition (SVD)", "focus": "Mathematical formula, singular values, U Σ V^T properties", "resource": "MIT 18.06 Gilbert Strang - Lec 29", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
            { "id": 27, "title": "Matrix Decomposition Problems", "focus": "Practice LU, QR, and SVD calculation", "resource": "Maths for ML Deisenroth - Chapter 4", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 28, "title": "Linear Algebra Subject Test", "focus": "Solve 30-question subject test. Analyze error log", "resource": "GATE Mock Series / Free PYQs", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
        ]
    },
    {
        "week": 5,
        "name": "Probability Basics & Bayes' Theorem",
        "phase": "phase1",
        "subject": "Probability & Statistics",
        "days": [
            { "id": 29, "title": "Sample Space, Events & Axioms", "focus": "Basic probability rules, Venn diagrams, set operations", "resource": "MIT OCW Probabilistic Systems - Lec 1", "url": "https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/" },
            { "id": 30, "title": "Permutations & Combinations in Prob.", "focus": "Counting principles, balls & bins, combinations selection", "resource": "Sheldon Ross Textbook - Chapter 1", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 31, "title": "Conditional Probability & Independence", "focus": "Multiplication rule, independent events definition", "resource": "MIT OCW Probabilistic Systems - Lec 2", "url": "https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/" },
            { "id": 32, "title": "Total Probability Theorem", "focus": "Partitioning sample space, weighted probabilities sum", "resource": "MIT OCW Probabilistic Systems - Lec 2", "url": "https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/" },
            { "id": 33, "title": "Bayes' Theorem", "focus": "Posterior probability calculation, base rate fallacy", "resource": "3Blue1Brown Bayes Theorem Video", "url": "https://www.youtube.com/watch?v=HZGCoVF3YvM" },
            { "id": 34, "title": "Bayes' Theorem Advanced Scenarios", "focus": "Multiple observations, conditional independence in Bayes", "resource": "GO Classes Probability Playlist", "url": "https://www.youtube.com/@Goclasses" },
            { "id": 35, "title": "Bayes' & Probability Practice", "focus": "Solve 20 problems on conditional probability", "resource": "GATE CSE PYQs on Probability", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
        ]
    },
    {
        "week": 6,
        "name": "Random Variables & Distributions",
        "phase": "phase1",
        "subject": "Probability & Statistics",
        "days": [
            { "id": 36, "title": "Discrete Random Variables (PMF, CDF)", "focus": "Probability mass function, cumulative steps, mean, variance", "resource": "MIT OCW Probabilistic Systems - Lec 3", "url": "https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/" },
            { "id": 37, "title": "Expectation & Variance Properties", "focus": "Linearity of expectation, scaling variance, moments", "resource": "Sheldon Ross Textbook - Chapter 4", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 38, "title": "Continuous Random Variables (PDF, CDF)", "focus": "Integration of density, cumulative distributions, mean, variance", "resource": "MIT OCW Probabilistic Systems - Lec 5", "url": "https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/" },
            { "id": 39, "title": "Binomial & Poisson Distributions", "focus": "Derivations, PMFs, mean, variance, Poisson approximation", "resource": "MIT OCW Probabilistic Systems - Lec 4", "url": "https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/" },
            { "id": 40, "title": "Uniform, Exponential & Geometric Dist.", "focus": "Memoryless property of exponential & geometric, integrations", "resource": "MIT OCW Probabilistic Systems - Lec 6", "url": "https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/" },
            { "id": 41, "title": "Normal (Gaussian) Distribution", "focus": "PDF, standard normal conversion, Z-table usage, properties", "resource": "MIT OCW Probabilistic Systems - Lec 7", "url": "https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/" },
            { "id": 42, "title": "Distribution Summary & Short Notes", "focus": "Write formula sheet for all distributions, solve 15 questions", "resource": "GO Classes Distribution Practice", "url": "https://www.youtube.com/@Goclasses" }
        ]
    },
    {
        "week": 7,
        "name": "Joint Distributions & Limit Theorems",
        "phase": "phase1",
        "subject": "Probability & Statistics",
        "days": [
            { "id": 43, "title": "Joint PMF & PDF", "focus": "Marginals, joint CDF, integration limits, double integration", "resource": "MIT OCW Probabilistic Systems - Lec 8", "url": "https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/" },
            { "id": 44, "title": "Conditional Distributions & Independence", "focus": "Independent random variables, conditional density", "resource": "Sheldon Ross Textbook - Chapter 6", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 45, "title": "Covariance & Correlation", "focus": "Mathematical formula, properties, correlation coefficient", "resource": "MIT OCW Probabilistic Systems - Lec 9", "url": "https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/" },
            { "id": 46, "title": "Sum of Independent Random Variables", "focus": "Convolutions of discrete and continuous variables", "resource": "MIT OCW Probabilistic Systems - Lec 10", "url": "https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/" },
            { "id": 47, "title": "Chebyshev's Inequality", "focus": "Bounding probability using mean and variance", "resource": "MIT OCW Probabilistic Systems - Lec 13", "url": "https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/" },
            { "id": 48, "title": "LLN & Central Limit Theorem", "focus": "Law of Large Numbers, CLT application to approximations", "resource": "MIT OCW Probabilistic Systems - Lec 14", "url": "https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/" },
            { "id": 49, "title": "Joint Distributions & Limits Practice", "focus": "Solve past GATE questions on CLT & Covariance", "resource": "GATE Math PYQ Papers", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
        ]
    },
    {
        "week": 8,
        "name": "Statistical Inference",
        "phase": "phase1",
        "subject": "Probability & Statistics",
        "days": [
            { "id": 50, "title": "Sampling Distributions", "focus": "Sample mean, sample variance, Chi-square & Student-t", "resource": "Walpole Stats Textbook - Chapter 8", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 51, "title": "Point Estimation & Bias", "focus": "Estimator definition, unbiasedness, Mean Squared Error", "resource": "NPTEL Statistical Inference", "url": "https://nptel.ac.in/courses/111105039" },
            { "id": 52, "title": "Maximum Likelihood Estimation (MLE)", "focus": "Likelihood functions, log-likelihood optimization, MLE steps", "resource": "GO Classes Stats MLE Lecture", "url": "https://www.youtube.com/@Goclasses" },
            { "id": 53, "title": "Hypothesis Testing Basics", "focus": "Null/Alternative, Type I & II errors, significance level", "resource": "NPTEL Hypothesis Testing", "url": "https://nptel.ac.in/courses/111105039" },
            { "id": 54, "title": "z-test & t-test Procedures", "focus": "One-sample, two-sample tests, critical values, p-value", "resource": "Walpole Stats Textbook - Chapter 10", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 55, "title": "Chi-Square Test & Likelihood Ratio", "focus": "Goodness of fit, independence tests", "resource": "NPTEL Statistical Inference - Lec 30", "url": "https://nptel.ac.in/courses/111105039" },
            { "id": 56, "title": "Probability & Stats Subject Test", "focus": "Practice full Statistics subject test, log mistakes", "resource": "GATE Mock Series", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
        ]
    },
    {
        "week": 9,
        "name": "Single-Variable Calculus",
        "phase": "phase1",
        "subject": "Calculus & Optimization",
        "days": [
            { "id": 57, "title": "Limits & Continuity", "focus": "L'Hopital's rule, continuity conditions, limits evaluations", "resource": "3Blue1Brown Calculus - Lec 1-3", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr" },
            { "id": 58, "title": "Differentiability of Functions", "focus": "Checking differentiability, left/right hand derivatives", "resource": "Thomas Calculus - Chapter 3", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 59, "title": "Mean Value Theorems", "focus": "Rolle's Theorem, Lagrange MVT, Cauchy MVT applications", "resource": "Thomas Calculus - Chapter 4", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 60, "title": "Taylor & Maclaurin Series", "focus": "Power series expansion, approximations, error term", "resource": "3Blue1Brown Calculus - Lec 11", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr" },
            { "id": 61, "title": "Single Variable Maxima & Minima", "focus": "First & second derivative tests, critical points", "resource": "Thomas Calculus - Chapter 4.5", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 62, "title": "Integration Basics & FTC", "focus": "Fundamental Theorem of Calculus, standard integrals", "resource": "3Blue1Brown Calculus - Lec 8", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr" },
            { "id": 63, "title": "Single-Variable Calculus Practice", "focus": "Solve 20 calculus questions from past GATE papers", "resource": "GATE Math PYQ Papers", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
        ]
    },
    {
        "week": 10,
        "name": "Multivariable Calculus & Optimization",
        "phase": "phase1",
        "subject": "Calculus & Optimization",
        "days": [
            { "id": 64, "title": "Partial Derivatives & Chain Rule", "focus": "Multivariable differentiation, total derivatives", "resource": "Thomas Calculus - Chapter 14", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 65, "title": "Gradient Vector & Directional Deriv.", "focus": "Computing gradient vector, geometrical interpretation", "resource": "3Blue1Brown Calculus - Lec 13", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr" },
            { "id": 66, "title": "Hessian Matrix & Taylor Exp", "focus": "Hessian calculation, quadratic form approximations", "resource": "Maths for ML Deisenroth - Chapter 5", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 67, "title": "Multivariable Maxima & Minima", "focus": "Saddle points, critical points checks using Hessian", "resource": "Thomas Calculus - Chapter 14.7", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 68, "title": "Unconstrained Optimization Basics", "focus": "Objective function, local vs global minima definition", "resource": "NPTEL Optimization Methods", "url": "https://nptel.ac.in/courses/111105039" },
            { "id": 69, "title": "Gradient Descent Algorithm", "focus": "Learning rate, updates, divergence, convergence criteria", "resource": "Maths for ML Deisenroth - Chapter 7", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 70, "title": "Calculus & Optimization Subject Test", "focus": "Complete optimization subject test, log mistakes", "resource": "GATE Mock Series", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
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
            { "id": 76, "title": "Arrays & Linked Lists (Python)", "focus": "Singly, doubly linked list ops, complexity comparison", "resource": "Goodrich Python DSA - Chapter 5-7", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 77, "title": "Python & Complexity Exercises", "focus": "Code snippet dry runs, find time complexity of codes", "resource": "GATE CSE Complexity Questions", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
        ]
    },
    {
        "week": 12,
        "name": "Trees, Graphs, Sorting & Searching",
        "phase": "phase2",
        "subject": "Programming & DSA",
        "days": [
            { "id": 78, "title": "Stacks & Queues", "focus": "Implementation using list/deque, applications (DFS/BFS)", "resource": "Goodrich Python DSA - Chapter 6", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 79, "title": "Binary Trees & Traversals", "focus": "Inorder, preorder, postorder traversals, reconstruction", "resource": "Madhavan Mukund DSA Python - Week 5", "url": "https://nptel.ac.in/courses/106106145" },
            { "id": 80, "title": "Binary Search Trees (BST) & Heaps", "focus": "Search property, insertion, min/max heap heapify ops", "resource": "Madhavan Mukund DSA Python - Week 6", "url": "https://nptel.ac.in/courses/106106145" },
            { "id": 81, "title": "Sorting Algorithms (Merge, Quick)", "focus": "Divide & conquer, pivot selections, average vs worst cases", "resource": "Madhavan Mukund DSA Python - Week 2", "url": "https://nptel.ac.in/courses/106106145" },
            { "id": 82, "title": "Heapsort, Bubble, Insert, Select", "focus": "Time/space complexities, stability of sorts", "resource": "Madhavan Mukund DSA Python - Week 3", "url": "https://nptel.ac.in/courses/106106145" },
            { "id": 83, "title": "Graphs Traversals (BFS & DFS)", "focus": "Adjacency matrix/list representation, BFS, DFS code", "resource": "Madhavan Mukund DSA Python - Week 7", "url": "https://nptel.ac.in/courses/106106145" },
            { "id": 84, "title": "DSA Subject Mock Test", "focus": "Take 30-question DSA quiz, record mistakes", "resource": "GATE Mock Series", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
        ]
    },
    {
        "week": 13,
        "name": "ER Model & Relational Algebra",
        "phase": "phase2",
        "subject": "DBMS & Warehousing",
        "days": [
            { "id": 85, "title": "Entity-Relationship (ER) Model", "focus": "Entities, attributes, primary key, relationships, mapping", "resource": "Amit Khurana DBMS - ER Model Playlist", "url": "https://www.youtube.com/@AmitKhurana" },
            { "id": 86, "title": "Relational Model Concepts", "focus": "Schema, relations, constraints (domain, referential integrity)", "resource": "NPTEL Database Design - Lec 5", "url": "https://nptel.ac.in/courses/106105175" },
            { "id": 87, "title": "Keys (Super, Candidate, Primary, Foreign)", "focus": "Identifying candidate keys from functional dependencies", "resource": "Amit Khurana DBMS Keys Lecture", "url": "https://www.youtube.com/@AmitKhurana" },
            { "id": 88, "title": "Relational Algebra Operations", "focus": "Selection, Projection, Join (Natural, Theta, Outer), Union", "resource": "NPTEL Relational Algebra", "url": "https://nptel.ac.in/courses/106105175" },
            { "id": 89, "title": "SQL Basics (SELECT, WHERE, GROUP BY)", "focus": "Query syntax, aggregates, having clause, filtering", "resource": "Amit Khurana SQL Playlist", "url": "https://www.youtube.com/@AmitKhurana" },
            { "id": 90, "title": "Advanced SQL (Joins & Subqueries)", "focus": "Nested queries, correlated subqueries, left/right outer joins", "resource": "NPTEL SQL Lectures", "url": "https://nptel.ac.in/courses/106105175" },
            { "id": 91, "title": "Relational Algebra & SQL Practice", "focus": "Solve 20 SQL/RA query translation problems", "resource": "GATE CSE DBMS PYQs", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
        ]
    },
    {
        "week": 14,
        "name": "Normalization, Transactions & Warehousing",
        "phase": "phase2",
        "subject": "DBMS & Warehousing",
        "days": [
            { "id": 92, "title": "Functional Dependencies", "focus": "FD rules, attribute closure, equivalence of FD sets", "resource": "Amit Khurana Normalization Playlist", "url": "https://www.youtube.com/@AmitKhurana" },
            { "id": 93, "title": "Normal Forms (1NF, 2NF, 3NF, BCNF)", "focus": "Lossless joins, dependency preservation, normal form check", "resource": "NPTEL Normalization Lectures", "url": "https://nptel.ac.in/courses/106105175" },
            { "id": 94, "title": "Transaction ACID Properties", "focus": "Atomicity, consistency, isolation, durability definitions", "resource": "Amit Khurana Transactions Playlist", "url": "https://www.youtube.com/@AmitKhurana" },
            { "id": 95, "title": "Serializability & Concurrency Control", "focus": "Conflict serializable check (precedence graph), view serializability", "resource": "NPTEL Concurrency Control", "url": "https://nptel.ac.in/courses/106105175" },
            { "id": 96, "title": "File Organization & B+ Trees", "focus": "Indexing concepts, B/B+ tree insertions & capacities", "resource": "Amit Khurana Indexing Lectures", "url": "https://www.youtube.com/@AmitKhurana" },
            { "id": 97, "title": "Data Warehousing Basics", "focus": "Star schema, snowflake schema, OLAP operations (Rollup, Drilldown)", "resource": "Gate Applied Course DBMS/DW Section", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 98, "title": "DBMS & DW Subject Test", "focus": "Solve 35 DBMS questions, check normalization & SQL solutions", "resource": "GATE Mock Series", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
        ]
    },
    {
        "week": 15,
        "name": "ML Basics & Regression Models",
        "phase": "phase3",
        "subject": "Machine Learning",
        "days": [
            { "id": 99, "title": "Introduction to Machine Learning", "focus": "Types of learning, generalization, under/overfitting", "resource": "Andrew Ng ML Coursera - Week 1", "url": "https://www.coursera.org/specializations/machine-learning-introduction" },
            { "id": 100, "title": "Bias-Variance Tradeoff", "focus": "Mathematical breakdown of MSE = Bias^2 + Var + Noise", "resource": "NPTEL Intro to ML - Lec 4", "url": "https://nptel.ac.in/courses/106106139" },
            { "id": 101, "title": "Simple Linear Regression", "focus": "OLS cost function, derivations of beta coefficients", "resource": "Andrew Ng ML Coursera - Week 2", "url": "https://www.coursera.org/specializations/machine-learning-introduction" },
            { "id": 102, "title": "Multiple Linear Regression & OLS", "focus": "Matrix formula β = (X^T X)^-1 X^T y derivation", "resource": "Aurélien Géron Chapter 4", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 103, "title": "Regularization (Lasso, Ridge)", "focus": "L1 and L2 penalties, geometrical explanation of sparsity", "resource": "NPTEL Intro to ML - Lec 8", "url": "https://nptel.ac.in/courses/106106139" },
            { "id": 104, "title": "Cross-Validation & Grid Search", "focus": "K-fold, stratified K-fold, hyperparameter tuning", "resource": "Andrew Ng ML Coursera - Week 3", "url": "https://www.coursera.org/specializations/machine-learning-introduction" },
            { "id": 105, "title": "Regression Practice Problems", "focus": "Compute gradient equations, regularized cost minimization", "resource": "Bishop PRML Exercises Chapter 3", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
        ]
    },
    {
        "week": 16,
        "name": "Classification Models & Decision Trees",
        "phase": "phase3",
        "subject": "Machine Learning",
        "days": [
            { "id": 106, "title": "Logistic Regression", "focus": "Sigmoid function, logistic loss function (cross-entropy)", "resource": "Andrew Ng ML Coursera - Week 4", "url": "https://www.coursera.org/specializations/machine-learning-introduction" },
            { "id": 107, "title": "Logistic Regression Decision Boundary", "focus": "Linear decision boundaries, multi-class softmax", "resource": "NPTEL Intro to ML - Lec 12", "url": "https://nptel.ac.in/courses/106106139" },
            { "id": 108, "title": "Support Vector Machines (Hard Margin)", "focus": "Maximizing the margin, constraint optimization formulation", "resource": "NPTEL Intro to ML - Lec 18", "url": "https://nptel.ac.in/courses/106106139" },
            { "id": 109, "title": "SVM Soft Margin & Kernel Trick", "focus": "Slack variables, dual form, RBF/polynomial kernels", "resource": "Andrew Ng ML Coursera - Week 7", "url": "https://www.coursera.org/specializations/machine-learning-introduction" },
            { "id": 110, "title": "Decision Trees Splitting Criteria", "focus": "Entropy, Gini impurity, Information Gain calculations", "resource": "NPTEL Intro to ML - Lec 15", "url": "https://nptel.ac.in/courses/106106139" },
            { "id": 111, "title": "Decision Tree Regressors & Pruning", "focus": "Variance reduction split, cost complexity pruning", "resource": "Aurélien Géron Chapter 6", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 112, "title": "Classification Models Practice", "focus": "Calculate entropy splits, trace SVM decision boundaries", "resource": "GATE DA 2024 ML Questions", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
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
            { "id": 118, "title": "Neural Networks Practice", "focus": "Perform forward/backprop calculations on mini-network", "resource": "GO Classes NN Tutorials", "url": "https://www.youtube.com/@Goclasses" },
            { "id": 119, "title": "Evaluation Metrics (ROC, AUC, F1)", "focus": "Precision, recall, confusion matrix, ROC-AUC plot", "resource": "Andrew Ng ML Coursera - Week 6", "url": "https://www.coursera.org/specializations/machine-learning-introduction" }
        ]
    },
    {
        "week": 18,
        "name": "Unsupervised Learning & PCA",
        "phase": "phase3",
        "subject": "Machine Learning",
        "days": [
            { "id": 120, "title": "K-Means Clustering", "focus": "K-means Lloyd's algorithm, objective function, initialization", "resource": "Andrew Ng ML Coursera - Week 8", "url": "https://www.coursera.org/specializations/machine-learning-introduction" },
            { "id": 121, "title": "K-Means Evaluation & Medoids", "focus": "Elbow method, silhouette score, k-medoids algorithm", "resource": "NPTEL Intro to ML - Lec 25", "url": "https://nptel.ac.in/courses/106106139" },
            { "id": 122, "title": "Hierarchical Clustering", "focus": "Agglomerative vs divisive, single, complete, average linkage", "resource": "NPTEL Intro to ML - Lec 26", "url": "https://nptel.ac.in/courses/106106139" },
            { "id": 123, "title": "PCA Concepts", "focus": "Dimensionality reduction, projection, variance maximization", "resource": "NPTEL Intro to ML - Lec 28", "url": "https://nptel.ac.in/courses/106106139" },
            { "id": 124, "title": "PCA Mathematical Derivation", "focus": "Covariance matrix, eigen decomposition, projection matrix", "resource": "Maths for ML Deisenroth - Chapter 10", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 125, "title": "Unsupervised Learning Practice", "focus": "Solve 15 problems on PCA & clustering", "resource": "GATE CSE/DA Math & ML PYQs", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 126, "title": "Machine Learning Subject Test", "focus": "Solve 35 ML questions, log accuracy and weak spots", "resource": "GATE Mock Series", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
        ]
    },
    {
        "week": 19,
        "name": "AI Search Strategies",
        "phase": "phase3",
        "subject": "Artificial Intelligence",
        "days": [
            { "id": 127, "title": "Uninformed Search (BFS, DFS)", "focus": "BFS & DFS properties, time and space complexity, completeness", "resource": "UC Berkeley CS188 - Lec 1", "url": "https://inst.eecs.berkeley.edu/~cs188/fa23/" },
            { "id": 128, "title": "Depth Limited & Iterative Deepening", "focus": "Space advantages of DFS with completeness of BFS", "resource": "Russell & Norvig Textbook - Chapter 3", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 129, "title": "Informed Search (Greedy Best First)", "focus": "Heuristic functions, search tree expansion strategy", "resource": "UC Berkeley CS188 - Lec 2", "url": "https://inst.eecs.berkeley.edu/~cs188/fa23/" },
            { "id": 130, "title": "A* Search", "focus": "A* completeness, heuristic admissibility (h(n) <= h*(n))", "resource": "NPTEL AI Search Methods - Lec 10", "url": "https://nptel.ac.in/courses/106105077" },
            { "id": 131, "title": "A* Consistency & Optimality", "focus": "Consistent heuristics, monotone property, optimality proofs", "resource": "NPTEL AI Search Methods - Lec 11", "url": "https://nptel.ac.in/courses/106105077" },
            { "id": 132, "title": "Minimax & Alpha-Beta Pruning", "focus": "Game trees, utility values, alpha-beta cutoffs", "resource": "UC Berkeley CS188 - Lec 3", "url": "https://inst.eecs.berkeley.edu/~cs188/fa23/" },
            { "id": 133, "title": "Search Algorithms Problems", "focus": "Solve game trees and calculate admissible A* heuristics", "resource": "GATE CSE AI PYQ Papers", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
        ]
    },
    {
        "week": 20,
        "name": "AI Logic & Uncertainty",
        "phase": "phase3",
        "subject": "Artificial Intelligence",
        "days": [
            { "id": 134, "title": "Propositional Logic Basics", "focus": "Conjunction, disjunction, implication, truth tables", "resource": "Russell & Norvig Textbook - Chapter 7", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 135, "title": "Propositional Inference", "focus": "Tautology, contradiction, resolution refutation proofs", "resource": "NPTEL AI Search/Logic - Lec 20", "url": "https://nptel.ac.in/courses/106105077" },
            { "id": 136, "title": "First-Order Logic (FOL)", "focus": "Quantifiers (Universal, Existential), predicates, functions", "resource": "Russell & Norvig Textbook - Chapter 8", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 137, "title": "FOL Inference & Unification", "focus": "Unification algorithm, Skolemization, resolution in FOL", "resource": "NPTEL AI Search/Logic - Lec 24", "url": "https://nptel.ac.in/courses/106105077" },
            { "id": 138, "title": "Bayesian Networks Syntax", "focus": "Graph structure, conditional probability tables (CPT)", "resource": "UC Berkeley CS188 - Lec 5", "url": "https://inst.eecs.berkeley.edu/~cs188/fa23/" },
            { "id": 139, "title": "Bayesian Networks Independence", "focus": "d-separation active/inactive paths, joint factorization", "resource": "UC Berkeley CS188 - Lec 6", "url": "https://inst.eecs.berkeley.edu/~cs188/fa23/" },
            { "id": 140, "title": "Artificial Intelligence Subject Test", "focus": "Complete AI subject test, check resolution and Bayes nets", "resource": "GATE Mock Series", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
        ]
    },
    {
        "week": 21,
        "name": "General Aptitude & Math Revision",
        "phase": "phase4",
        "subject": "Revision",
        "days": [
            { "id": 141, "title": "Quantitative Aptitude (Ratios, %)", "focus": "Percentages, ratios, time-work, speed-distance", "resource": "GATE General Aptitude Resources", "url": "https://www.geeksforgeeks.org/gate-general-aptitude/" },
            { "id": 142, "title": "Aptitude Combinatorics & Stats", "focus": "Basic permutations, probability, mean-median-mode GA", "resource": "GATE GA Playlists", "url": "https://www.youtube.com/" },
            { "id": 143, "title": "Spatial Aptitude & Verbal", "focus": "Paper folding, shape rotations, English grammar, synonyms", "resource": "GATE GA Playlists", "url": "https://www.youtube.com/" },
            { "id": 144, "title": "Linear Algebra Formulas Review", "focus": "Four subspaces, eigenvalues, QR, SVD formula cards", "resource": "Linear Algebra Cheat Sheets", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 145, "title": "Probability Distributions Review", "focus": "Continuous/Discrete formula sheets, CLT bounds", "resource": "Probability Cheat Sheets", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 146, "title": "Calculus & Optimization Review", "focus": "Hessian matrix test, gradient descent update steps", "resource": "Calculus Cheat Sheets", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 147, "title": "Math & Aptitude Combined Test", "focus": "Take 40-question Math & GA combined mock test", "resource": "GATE Mock Series", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
        ]
    },
    {
        "week": 22,
        "name": "Core CS & ML/AI Revision",
        "phase": "phase4",
        "subject": "Revision",
        "days": [
            { "id": 148, "title": "Programming & Complexity Review", "focus": "Recursion trees, Master method, sorting bounds", "resource": "DSA Cheat Sheets", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 149, "title": "Data Structures & Graphs Review", "focus": "Tree traversals, heap ops, Graph DFS/BFS codes", "resource": "DSA Cheat Sheets", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 150, "title": "DBMS SQL & Normalization Review", "focus": "Checking normal forms, transactions serializability graphs", "resource": "DBMS Cheat Sheets", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 151, "title": "Machine Learning Regression & SVM Review", "focus": "OLS formula, L1/L2 shapes, SVM margin formulas", "resource": "ML Cheat Sheets", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 152, "title": "ML Trees & Neural Networks Review", "focus": "Information gain, backprop chain rule steps", "resource": "ML Cheat Sheets", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 153, "title": "AI Search & Logic Review", "focus": "A* heuristics consistency, resolution rules FOL", "resource": "AI Cheat Sheets", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 154, "title": "CS & ML/AI Combined Revision Test", "focus": "Take 40-question technical combined test", "resource": "GATE Mock Series", "url": "https://ds-ai-gate.github.io/dsai-gate/" }
        ]
    },
    {
        "week": 23,
        "name": "Solve Official GATE DA PYQ Papers",
        "phase": "phase4",
        "subject": "Mock Prep",
        "days": [
            { "id": 155, "title": "Solve GATE DA 2024 - Part 1", "focus": "Attempt first 30 questions under 1.5 hours", "resource": "Official GATE DA 2024 Paper", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 156, "title": "Solve GATE DA 2024 - Part 2", "focus": "Attempt remaining 35 questions", "resource": "Official GATE DA 2024 Paper", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 157, "title": "Thorough Analysis of 2024 Paper", "focus": "Check solutions, write down wrong questions in Mistake Book", "resource": "GATE DA 2024 Video Analysis", "url": "https://www.youtube.com/" },
            { "id": 158, "title": "Solve GATE DA 2025 - Part 1", "focus": "Attempt first 30 questions under exam conditions", "resource": "Official GATE DA 2025 Paper", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 159, "title": "Solve GATE DA 2025 - Part 2", "focus": "Attempt remaining 35 questions", "resource": "Official GATE DA 2025 Paper", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 160, "title": "Thorough Analysis of 2025 Paper", "focus": "Analyze error patterns, calculate total raw score", "resource": "GATE DA 2025 Video Analysis", "url": "https://www.youtube.com/" },
            { "id": 161, "title": "Mistake Book Sunday Review", "focus": "Re-solve all questions logged in your Mistake Book", "resource": "Personal Notes", "url": "" }
        ]
    },
    {
        "week": 24,
        "name": "Mock Tests & Short Notes Compile",
        "phase": "phase4",
        "subject": "Mock Prep",
        "days": [
            { "id": 162, "title": "Full Length Mock 1", "focus": "Attempt 3-hour mock. Focus on question selection", "resource": "Mock Series Provider", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 163, "title": "Analyze Mock 1 & Revise", "focus": "Error analysis: mathematical slips vs conceptual gaps", "resource": "Personal Notes", "url": "" },
            { "id": 164, "title": "Full Length Mock 2", "focus": "Attempt 3-hour mock. Improve time allocation", "resource": "Mock Series Provider", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
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
            { "id": 169, "title": "Full Length Mock 3", "focus": "Complete mock under simulated GATE timing (9 AM - 12 PM)", "resource": "Mock Series Provider", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 170, "title": "Analyze Mock 3 & Target Revision", "focus": "Revise Bayesian nets and eigenvalues", "resource": "Personal Notes", "url": "" },
            { "id": 171, "title": "Full Length Mock 4", "focus": "Complete mock under simulated GATE timing", "resource": "Mock Series Provider", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
            { "id": 172, "title": "Analyze Mock 4 & Target Revision", "focus": "Revise A* search heuristics conditions", "resource": "Personal Notes", "url": "" },
            { "id": 173, "title": "Full Length Mock 5", "focus": "Final score calibration mock", "resource": "Mock Series Provider", "url": "https://ds-ai-gate.github.io/dsai-gate/" },
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
    { "category": "math", "name": "Gilbert Strang MIT 18.06 Lectures", "type": "YouTube Playlist", "url": "https://www.youtube.com/playlist?list=PL49CF3715CB72B641" },
    { "category": "math", "name": "3Blue1Brown Essence of Linear Algebra", "type": "YouTube Visualizations", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab" },
    { "category": "math", "name": "MIT 6.041 Probabilistic Systems Analysis", "type": "MIT OpenCourseWare", "url": "https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/" },
    { "category": "math", "name": "GO Classes GATE DA Playlists", "type": "YouTube Channel", "url": "https://www.youtube.com/@Goclasses" },
    { "category": "math", "name": "Mathematics for Machine Learning Textbook", "type": "PDF / Free Book Chapters", "url": "https://mml-book.github.io/" },
    { "category": "math", "name": "3Blue1Brown Essence of Calculus", "type": "YouTube Playlist", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr" },
    { "category": "cs", "name": "NPTEL Programming & Data Structures in Python", "type": "NPTEL Course Lectures", "url": "https://nptel.ac.in/courses/106106145" },
    { "category": "cs", "name": "Amit Khurana DBMS Lectures", "type": "YouTube Playlist", "url": "https://www.youtube.com/@AmitKhurana" },
    { "category": "cs", "name": "NPTEL Database System Concepts (IITM)", "type": "NPTEL Course", "url": "https://nptel.ac.in/courses/106105175" },
    { "category": "cs", "name": "GeeksforGeeks GATE CS & DA Notes", "type": "Written Tutorials", "url": "https://www.geeksforgeeks.org/gate-ds-ai-syllabus/" },
    { "category": "ml-ai", "name": "Andrew Ng Machine Learning Specialization", "type": "Coursera (Audit Mode)", "url": "https://www.coursera.org/specializations/machine-learning-introduction" },
    { "category": "ml-ai", "name": "NPTEL Introduction to Machine Learning (IITM)", "type": "NPTEL Course Lectures", "url": "https://nptel.ac.in/courses/106106139" },
    { "category": "ml-ai", "name": "UC Berkeley CS188 Artificial Intelligence", "type": "UC Berkeley Course Website", "url": "https://inst.eecs.berkeley.edu/~cs188/fa23/" },
    { "category": "ml-ai", "name": "NPTEL Artificial Intelligence Search Methods", "type": "NPTEL Course", "url": "https://nptel.ac.in/courses/106105077" },
    { "category": "ml-ai", "name": "3Blue1Brown Neural Networks Intuition", "type": "YouTube Videos", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000DX_ZCJB-3Ky" },
    { "category": "ml-ai", "name": "DS-AI-GATE Curated Notes Hub", "type": "GitHub Repository", "url": "https://github.com/DS-AI-GATE/dsai-gate" }
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
        "mocks": []
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

# ==========================================
# 6. Tabbed View Navigation
# ==========================================
tabs = st.tabs(["📅 Study Planner", "📋 Syllabus Tracker", "📚 Free Resources", "📝 Mock Tests Log", "📈 Performance Analytics"])

# ------------------------------------------
# Tab 1: Study Planner
# ------------------------------------------
with tabs[0]:
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
                
                st.markdown("<hr style='margin:10px 0; border:0; border-top:1px solid rgba(255,255,255,0.04);'>", unsafe_allow_html=True)

# ------------------------------------------
# Tab 2: Syllabus Tracker
# ------------------------------------------
with tabs[1]:
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
with tabs[2]:
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
with tabs[3]:
    st.subheader("Mock Test Log Book")
    
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

# ------------------------------------------
# Tab 5: Performance Analytics
# ------------------------------------------
with tabs[4]:
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

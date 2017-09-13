#!/bin/bash
# Compile the code
#javac DecisionTrees/*.java
# Run for each question
echo "========================"
echo "Question 1(c)"
echo "========================"
#java -cp DecisionTrees MainClass Dataset/updated_train.txt Dataset/updated_train.txt 
# python DecisionTrees.py Dataset/updated_train.txt Dataset/updated_train.txt
# python3.5 DecisionTrees.py Dataset/updated_train.txt Dataset/updated_train.txt
python3.6 Id3AlgoFinal.py Dataset/updated_train.txt Dataset/updated_train.txt
echo "========================"
echo
echo

echo "========================"
echo "Question 1(d)"
echo "========================"
#java -cp DecisionTrees MainClass Dataset/updated_train.txt Dataset/updated_test.txt 
# python DecisionTrees.py Dataset/updated_train.txt Dataset/updated_test.txt 
# python3.5 DecisionTrees.py Dataset/updated_train.txt Dataset/updated_test.txt 
python3.6 Id3AlgoFinal.py Dataset/updated_train.txt Dataset/updated_test.txt 
echo "========================"
echo
echo

echo "========================"
echo "Question 2"
echo "========================"
#java -cp DecisionTrees MainClass Dataset/updated_train.txt Dataset/updated_test.txt Dataset/Updated_CVSplits 1 2 3 4 5 10 15 20 
# python DecisionTrees.py Dataset/updated_train.txt Dataset/updated_test.txt Dataset/Updated_CVSplits 1 2 3 4 5 10 15 20 
# python3.5 DecisionTrees.py Dataset/updated_train.txt Dataset/updated_test.txt Dataset/Updated_CVSplits 1 2 3 4 5 10 15 20 
# python3/6 DecisionTrees.py Dataset/updated_train.txt Dataset/updated_test.txt Dataset/Updated_CVSplits 1 2 3 4 5 10 15 20 
echo "========================"
echo
echo
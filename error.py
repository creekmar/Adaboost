

def main():
    answers = "test_answers.txt"
    test = "out.txt"
    answers = open(answers)
    test = open(test)
    incorrect = 0
    total = 0
    for line in answers:
        line = line.strip().upper()
        line2 = test.readline().strip().upper()
        if line != line2:
            incorrect += 1
        total += 1
    print(incorrect/total)
    answers.close()
    test.close()


if __name__ == '__main__':
    main()

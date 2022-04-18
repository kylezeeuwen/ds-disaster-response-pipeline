def evaluate_single_classifier(y_actual, y_predictions):
    '''
    INPUT:
    y_actual - array - actual results
    y_predictions - array - predictions

    OUTPUT:
    metrics - a series of performance metrics
    '''

    TP = 0
    FP = 0
    TN = 0
    FN = 0
    P = 0
    N = 0

    for i in range(len(y_predictions)):
        if y_actual[i] == 1:
            P += 1
        if y_actual[i] == 0:
            N += 1
        if y_actual[i] == y_predictions[i] == 1:
            TP += 1
        if y_predictions[i] == 1 and y_actual[i] != y_predictions[i]:
            FP += 1
        if y_actual[i] == y_predictions[i] == 0:
            TN += 1
        if y_predictions[i] == 0 and y_actual[i] != y_predictions[i]:
            FN += 1

    # source: https://en.wikipedia.org/wiki/Sensitivity_and_specificity
    # sensitivity, recall, hit rate, or true positive rate (TPR)
    TPR = divide_or_zero(TP, P)

    # specificity, selectivity or true negative rate (TNR)
    TNR = divide_or_zero(TN, N)

    # precision or positive predictive value (PPV)
    PPV = divide_or_zero(TP, (TP + FP))

    # ____ or negative predictive value (PPV)
    NPV = divide_or_zero(TN, (TN + FN))

    # accuracy
    ACC = divide_or_zero((TP + TN), (P + N))

    return {
        "P": P,
        "N": N,
        "TP": TP,
        "FP": FP,
        "TN": TN,
        "FN": FN,
        "TPR": TPR,
        "TNR": TNR,
        "PPV": PPV,
        "NPV": NPV,
        "ACC": ACC,
    }

def divide_or_zero(numerator, denominator):
    '''
    INPUT:
    numerator - numeric
    denominator - numeric

    OUTPUT:
    numeric

    Divide numerator by denominotor, unless denominator is 0 then just return 0
    '''
    return numerator / denominator if denominator != 0 else 0

def custom_f1_scorer_with_recall_favored(y, y_pred, **kwargs):
    beta=3
    category_names = y.columns

    f1 = []
    for idx, category in enumerate(category_names):
        y_actual_single_classification = y[category].tolist()
        y_pred_single_classification = y_pred[:, idx]
        single_classifier_metrics = evaluate_single_classifier(
            y_actual_single_classification,
            y_pred_single_classification
        )

        precision = single_classifier_metrics['PPV']
        recall = single_classifier_metrics['TPR']

        f1.append(divide_or_zero(
            (1 + beta*beta) * (precision*recall),
            ((beta*beta*precision) + recall))
        )
    print(f1)
    return sum(f1) / len(category_names)
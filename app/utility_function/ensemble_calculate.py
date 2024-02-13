import numpy as np

def ensemble(vessel, quan_predict_result, quan_predict_prop, qual_predict_result, qual_predict_prop, model_quanti_acc, model_quali_acc):
    print("-" * 25, f"Ensemble {vessel.upper()}", "-" * 25)
    predict_result  = np.array([quan_predict_result, qual_predict_result])
    predict_prop    = np.array([quan_predict_prop * model_quanti_acc, qual_predict_prop * model_quali_acc])

    print(f"\t>>>>> Calculate Quantitative ({quan_predict_result}): {quan_predict_prop} * {model_quanti_acc}\t= {quan_predict_prop * model_quanti_acc}")
    print(f"\t>>>>> Calculate Qualitative  ({qual_predict_result}): {qual_predict_prop} * {model_quali_acc}\t= {qual_predict_prop * model_quali_acc}")

    # print(f"\t>>>>> predict_result: {predict_result}")
    # print(f"\t>>>>> predict_prop: {predict_prop}")
    print(f"\t>>>>> result: {predict_result[np.argmax(predict_prop)], np.max(predict_prop)}")

    return int(predict_result[np.argmax(predict_prop)]), float(np.max(predict_prop))
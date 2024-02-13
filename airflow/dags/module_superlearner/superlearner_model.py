
from sklearn.base import BaseEstimator, ClassifierMixin

# Add more packages as required

# import all classfier methods and metrics
from sklearn import ensemble
from sklearn import tree
from sklearn import linear_model
from sklearn import neighbors
from sklearn import svm

# from sklearn.model_selection import train_test_split
# from sklearn import cross_validation
from sklearn import clone
from sklearn import metrics

#import selection method
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
# from sklearn.model_selection import cross_val_score
# from sklearn.model_selection import train_test_split

#import validation and others
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.utils.multiclass import unique_labels
from sklearn.tree import export_graphviz

#other utility packages
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import pyplot
from random import randint
# from scipy.spatial import distance




# Create a new classifier which is based on the sckit-learn BaseEstimator and ClassifierMixin classes
class SuperLearnerClassifier(BaseEstimator, ClassifierMixin):
    
    """An ensemble classifier that uses heterogeneous models at the base layer and a aggregation model at the 
    aggregation layer. A k-fold cross validation is used to generate training data for the stack layer model.

    Parameters
    ----------
    n_classes: integer, required (especially when setting proba_2train_meta = True)   
        The number of target classes for prediction, used to construct an array to store the prbability output from base classifiers
        
    estimators: list of BaseEstimators, optional (default = 6 base estimators, including:  
            1) DecisionTreeClassifier with max_depth = 10,
            2) ExtraTreeClassifier,
            3) LogisticRegression,
            4) Support Vector Machine - NuSVC,
            5) Support Vector Machine - SVC,
            6) KNeighborsClassifier with n_neighbors = 5)
        A list of scikit-learn base estimators with fit() and predict() methods.
        
    cv_folds: integer, optional (default = 5)
        The number of k to perform k-fold cross validation to be used. 
    
    proba_2train_meta: boolean, optional (default = False)
        A boolean flag variable to specify the meta learner at the stacked level should be trained either on label output or probability output.
            False => trained on 'label output' - Typical Super learner classifier, using Stack Layer Training Set (Labels)
            True => train on 'probability output' - using Stack Layer Training Set (Probabilities)
    
    ori_input_2train_meta: boolean , optional (default = False)
        A boolean flag variable to specify whether the meta learner should be trained on the training set with original features or not.
            False => trained only on 'output' from base estimators 
            True => train on 'original features/inputs' plus 'output' from base estimators
    
    meta_model_type: string, optional (default = "DCT")
        An option in string, only either "DCT" or "LR", to specify the type of model to use at the stack layer for a meta learner
            "DCT" => DecisionTreeClassifier
            "LR" => LogisticRegression
    
    est_accuracy: boolean, optional (default = False) - only available when proba_2train_meta = False
        A boolean flag variable to analyse and print the Mean Accuracy (MA) as the strength/performance of base estimators (predictive power). 
            False => do nothing
            True => analyse and print the mean accuracy
  
    est_corr: boolean, optional (default = False) - only available when proba_2train_meta = False
        A boolean flag variable to analyse and print the Pearson correlation between base estimators (diversity).
            False => do nothing
            True => analyse and print the Pearson correlation between base estimators
    
    debug_mode: boolean, optional (default = False)
        A boolean flag variable to set the verbose mode in printing debugging info via the "_print_debug" function
            
    Attributes
    ----------
    n_classes: integer   
        The number of target classes for prediction, used to expand an array to store the prbability output from base classifiers
        
    estimators: list
        A list of BaseEstimators used  
    
    cv_folds: integer
        the number of k to perform cross validation used 
    
    proba_2train_meta: boolean
        the flag variable to select the Stack Layer Training Set to be Labels (False) or Probabilities (True)
        
    ori_input_2train_meta: boolean
        the flag variable to include the original features/inputs in the Stack Layer Training Set: not include (False) or include (True)
    
    meta_model_type: string
        the option variable for the type of model of the meta-learner at the stack layer 
    
    est_accuracy: boolean
        the flag variable to perform and print an analysis of Mean Accuracy (MA) of base estimators: not perform (False) or perform (True)
        
    est_corr: boolean
        the flag variable to perform and print an analysis of Pearson correlation between base estimators: not perform (False) or perform (True)
        
    debug_mode: boolean
        The flag variable to print debugging info via the "_print_debug" function
    
    Notes
    -----
    

    See also
    --------
    
    ----------
    .. [1]  van der Laan, M., Polley, E. & Hubbard, A. (2007). 
            Super Learner. Statistical Applications in Genetics 
            and Molecular Biology, 6(1) 
            doi:10.2202/1544-6115.1309
    Examples
    --------
    >>> from sklearn.datasets import load_iris
    >>> from sklearn.model_selection import cross_val_score
    >>> clf = SuperLearnerClassifier()
    >>> iris = load_iris()
    >>> cross_val_score(clf, iris.data, iris.target, cv=10)

    """
    # Constructor for the classifier object
    def __init__(self,
                 n_classes,
                 estimators = [tree.DecisionTreeClassifier(criterion = "entropy", max_depth = 10),
                               tree.ExtraTreeClassifier(),
                               linear_model.LogisticRegression(max_iter=2000),
                               svm.NuSVC(probability=True), 
                               svm.SVC(probability=True),
                               neighbors.KNeighborsClassifier(n_neighbors = 5)
                              ], 
                 cv_folds = 5,                   # To avoid overfiiting of the stacked level classifier, specify the number of K for k-fold cross validation in level-one base classifiers   
                 proba_2train_meta = False,      # Specify whether the stacked layer classifier should be trained on probability output from the base classifiers or not; if not, trained on label outputs
                 ori_input_2train_meta = False,  # Specify whether the original input is added, together with the output from the base classifiers, to train the stacked layer classifier
                 meta_model_type = "DCT",        # Specify the model type at the stacked layer either Decision Tree or Logistic Regression, meta_model_type = {"DCT", "LR"}
                 est_accuracy = False,
                 est_corr = False,
                 debug_mode = False):
        
        # throw exceptions to check validity of parameters  
        if not isinstance(n_classes, int):
            raise TypeError("Please set the \'n_classes\' in integer, to specify the number of target classes for prediction.")
        if not (meta_model_type == "DCT" or meta_model_type == "LR"):
            raise ValueError("In the current support of a meta learner, \'meta_model_type\' must be only \'DCT\' for DecisionTreeClassifier or \'LR\' for LogisticRegression.")
        if len(estimators) < 5 or len(estimators) > 10:
            raise ValueError("It is sensible to use a set of 5-10 algorithms as base learners. The current number of base estimators is: " + str(len(estimators)))
        
        self.n_classes = n_classes        
        self.estimators = estimators    
        self.cv_folds = cv_folds
        self.proba_2train_meta = proba_2train_meta
        self.ori_input_2train_meta = ori_input_2train_meta
        self.meta_model_type = meta_model_type
        self.est_accuracy = est_accuracy
        self.est_corr = est_corr
        self.debug_mode = debug_mode

            
    # The fit function to train a classifier
    def fit(self, X, y):
        """Build a SuperLearner classifier from the training set (X, y).
        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]
            The training input samples. 
        y : array-like, shape = [n_samples] 
            The target values (class labels) as integers or strings.
        Returns
        -------
        self : object
        """     
        # Check that X and y have correct shape
        X, y = check_X_y(X, y)
        
        n_estimators = len(self.estimators)
        # At the stacked layer, use a decision tree model as a default (stacked layer classifier, aka. meta learner)
        self.meta_learner = None
        if self.meta_model_type == "DCT":
            self.meta_learner = tree.DecisionTreeClassifier(criterion = "entropy", max_depth = 10)
        elif self.meta_model_type == "LR":
            self.meta_learner = linear_model.LogisticRegression()
            
        #1. split data into k blocks using k-fold cross calidation
        n_example = len(y)
        # folds = cross_validation.KFold(n_example, self.cv_folds)
        kf = KFold(n_splits = self.cv_folds)
        folds = kf.split(X)
        print(folds)
        
        #2. train each cadidate learner/estimator using k-fold cross calidation
        y_pred_cv = None
        # -----------------------Using "label" output to train a meta-learner at stacked level-----------------------
        if not self.proba_2train_meta:
            self._print_debug("--Using \'labels\' to train the meta-learner")
            # *****Create a 2D array, called “level-one” data, to store predicted results, as shown in L04 note, page 20***** 
            y_pred_cv = np.empty(shape=(n_example, n_estimators)) 
            est_accuracies = np.zeros(n_estimators)
            cv_index = 1
            
            for train_index, test_index in folds:
                X_train, X_test = X[train_index], X[test_index]
                y_train, y_test = y[train_index], y[test_index]
                
                #2.1 perform train each learner/estimator one by one in a list, estimators
                if self.est_accuracy:
                    print("--------cross validation:", cv_index, "------------")
                    cv_index+=1
                    
                for est_index in range(n_estimators):
                    estimator = clone(self.estimators[est_index])
                
                    estimator.fit(X_train, y_train)
                    #2.2 *****get predicted results from each estimator and put it into array*****
                    est_pred = estimator.predict(X_test)
                
                    #==========================Analyse Accuracy==========================
                    if self.est_accuracy:
                        accuracy = metrics.accuracy_score(y_test, est_pred)
                        est_name = str(type(estimator))
                        print("Accuracy of" , est_name[est_name.rfind(".")+1:est_name.rfind("'")], ":", accuracy) 
                        est_accuracies[est_index] += accuracy
                    
                    y_pred_cv[test_index, est_index] = est_pred
            
            #==========================Compute Mean Accuracy==========================
            if self.est_accuracy:
                print("")
                print("=====Overall Performance of Each Estimator=====")
                for est_index in range(n_estimators):
                    mean_accuracy = est_accuracies[est_index] / float(self.cv_folds)
                    est_name = str(type(self.estimators[est_index]))
                    print("Mean Accuracy of" , est_name[est_name.rfind(".")+1:est_name.rfind("'")], ":", mean_accuracy) 
                print("===============================================")
                print("")
            
            if self.est_corr:
                print("")
                print("--------------Correlation Matrix---------------")
                est_names = []
                for est_index in range(n_estimators):
                    est_name = str(type(self.estimators[est_index]))
                    est_names.append(est_name[est_name.rfind(".")+1:est_name.rfind("'")])
                df = pd.DataFrame(data=y_pred_cv[0:,0:],    # values
                             #index=data[1:,0],    # 1st column as index
                             columns=est_names[0:]) 
                
                corr_matrix = df.corr(method='pearson')
                display(corr_matrix)
                
                print("----------Mean of a Correlation Matrix----------")
                #print(corr_matrix.values[np.triu_indices_from(corr_matrix.values,1)].mean())
                corr_matrix2 = corr_matrix.copy()
                corr_matrix2.values[np.tril_indices_from(corr_matrix2)] = np.nan
                #display(corr_matrix2)
                print("Mean of a Correlation Matrix:", corr_matrix2.unstack().mean())
                print("================================================")
                print("")

                
        # -------------------Using "probability" output to train a meta-learner at stacked level---------------------
        else:
            self._print_debug("--Using \'probabilities\' to train the meta-learner")
            # *****Create a 3D array, called “level-one” data, to store predicted results, as shown in L04 note, page 20***** 
            y_pred_cv = np.empty(shape=(n_example, n_estimators, self.n_classes)) 
            for train_index, test_index in folds:
                X_train, X_test = X[train_index], X[test_index]
                y_train, y_test = y[train_index], y[test_index]
                
                #2.1 perform train each learner/estimator one by one in a list, estimators
                for est_index in range(n_estimators):
                    estimator = clone(self.estimators[est_index])
                
                    estimator.fit(X_train, y_train)
                    #2.2 *****get predicted probability results from each estimator and put it into array*****
                    est_pred = estimator.predict_proba(X_test)
                               
                    y_pred_cv[test_index, est_index] = est_pred
            
            # *****Reshape to 2D array when using probability to train a meta-learner, in which a training metrix includes the probabilities of each class*****
            y_pred_cv = y_pred_cv.reshape(n_example , n_estimators * self.n_classes)
        
        if self.ori_input_2train_meta:
            self._print_debug("--Added \'original input\' to train a meta-learner")
            y_pred_cv = np.c_[X, y_pred_cv]
        
        #3. At the stacked layer, train the metalearner using a decision tree model (default: DCT) or logistic regrssion (LR) on the level-one data 
        self.meta_learner.fit(y_pred_cv, y)
        
        #0. Train each cadidate learner/estimator on "entire dataset" as a fitted estimator to perform a level-one prediction in a "predict" function
        self.fitted_estimators = clone(self.estimators)
        for fitted_estimator in self.fitted_estimators:
            fitted_estimator.fit(X, y)
            
        if isinstance(self.meta_learner, tree.DecisionTreeClassifier):   
            self._print_debug("--Meta learner: Decision Tree")
        elif isinstance(self.meta_learner, linear_model.LogisticRegression):
            self._print_debug("--Meta learner: Logistic Regression")
            
        return self

    

    # The predict function to make a set of predictions for a set of query instances
    def predict(self, X):
        """Predict class labels of the input samples X.
        Parameters
        ----------
        X : array-like matrix of shape = [n_samples, n_features]
            The input samples. 
        Returns
        -------
        p : array of shape = [n_samples, ].
            The predicted class labels of the input samples. 
        """
        #4. Generate predictions from all of the base learners
        y_pred_all = self._level_one_predict(X)
        
        #5. Feed those predictions into the meta-learner to generate the ensemble prediction as "class labels".
        y_pred = self.meta_learner.predict(y_pred_all)
         
        if isinstance(self.meta_learner, tree.DecisionTreeClassifier):   
            self._print_debug("Meta learner: Decision Tree")
        elif isinstance(self.meta_learner, linear_model.LogisticRegression):
            self._print_debug("Meta learner: Logistic Regression")
            
        return y_pred

    
    # The predict function to make a set of predictions for a set of query instances
    def predict_proba(self, X):
        """Predict class probabilities of the input samples X.
        Parameters
        ----------
        X : array-like matrix of shape = [n_samples, n_features]
            The input samples. 
        Returns
        -------
        p : array of shape = [n_samples, n_labels].
            The predicted class label probabilities of the input samples. 
        """
        
        #4. Generate predictions from all of the base learners
        y_pred_all = self._level_one_predict(X)
           
        #5. Feed those predictions into the metalearner to generate the ensemble prediction as "class label prababilities".
        y_pred = self.meta_learner.predict_proba(y_pred_all)
         
        if isinstance(self.meta_learner, tree.DecisionTreeClassifier):   
            self._print_debug("Meta learner: Decision Tree")
        elif isinstance(self.meta_learner, linear_model.LogisticRegression):
            self._print_debug("Meta learner: Logistic Regression")
            
        return y_pred

    # a private function to generate predictions from all of the base learners. This function is called by two common functions, i.e., "predict" and "predict_proba" functions 
    def _level_one_predict(self, X):
        n_estimators = len(self.estimators)
        
        #4. Generate predictions from all of the base learners, to be used to feed to a stacked level classifier
        n_X = X.shape[0]
        y_pred_all = None
        # -----------------------Feed "label" output to a meta-learner at stacked level-----------------------
        if not self.proba_2train_meta:
            self._print_debug("Feed \'label\' outputs to the meta-learner")
            # *****Create a 2D array, called “level-one” data, to store predicted results, as shown in L04 note, page 20***** 
            y_pred_all = np.empty((n_X, n_estimators))
            for est_index in range(n_estimators):
                y_pred_all[:,est_index] = self.fitted_estimators[est_index].predict(X)
        # --------------------Feed "probability" output to a meta-learner at stacked level--------------------
        else:
            self._print_debug("Feed \'probability\' outputs to the meta-learner")
            # *****Create a 3D array, called “level-one” data, to store predicted results, as shown in L04 note, page 20***** 
            y_pred_all = np.empty(shape=(n_X, n_estimators, self.n_classes)) 
            for est_index in range(n_estimators):
                y_pred_all[:,est_index] = self.fitted_estimators[est_index].predict_proba(X)
            
            # Reshape to 2D array to feed the given probability to the meta-learner
            y_pred_all = y_pred_all.reshape(n_X , n_estimators * self.n_classes)     
                 
        if self.ori_input_2train_meta:
            self._print_debug("Added \'original input\' to feed to a meta-learner")
            y_pred_all = np.c_[X, y_pred_all]
        
        return y_pred_all
    
    # a private function to print debug output
    def _print_debug(self, output):
        if self.debug_mode:
            display(output)

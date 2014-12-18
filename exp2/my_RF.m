function  [Tr_acc, Te_acc, tmp_precision, tmp_recall, tmp_f1_score] = my_RF(Tr, Te, nTrees)

train_features = Tr(:,2:end);
train_target = Tr(:,1);
test_features = Te(:,2:end);
label_Actual_whole = Te(:,1);

B = TreeBagger(nTrees,train_features,train_target,'Method','classification');
Y = B.predict(test_features)

label_Expected_whole = Y

Tr_acc =  0
te_acc = length(find(label_Expected_whole==label_Actual_whole))
positives_Actural = length(find(label_Actual_whole==1))
positives_Expected = length(find(label_Expected_whole==1))
positives_correct = length(find(label_Expected_whole==label_Actual_whole & label_Actual_whole==1))
precision = positives_correct/positives_Actural
recall = positives_correct/positives_Expected
f1_score = 2*precision*recall/(precision+recall)

end
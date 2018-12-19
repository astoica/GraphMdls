library(lda)

dat1 = readLines("~/Downloads/documents1000.csv")
docs <- lexicalize(dat1, sep=",", lower=TRUE, count=1L, vocab=NULL)

#to.keep <- docs$vocab[word.counts(docs$documents, docs$vocab) >= 2]

#docs <- lexicalize(dat1, lower=TRUE, vocab=to.keep)

set.seed(8675309)
gender = readLines("~/Downloads/documents1000-gender-binary.csv")

num.topics <- 20
params <- sample(c(-1, 1), num.topics, replace=TRUE)
result <- slda.em(documents=docs$documents, K=num.topics, vocab=docs$vocab, num.e.iterations=10, num.m.iterations=4, alpha=1.0, eta=1.0, gender, params, variance=0.25, lambda=1.0, logistic=FALSE, method="sLDA")

require("ggplot2")

Topics <- apply(top.topic.words(result$topics, 5, by.score=TRUE), 2, paste, collapse=" ")
coefs <- data.frame(coef(summary(result$model)))

theme_set(theme_bw())

coefs <- cbind(coefs, Topics=factor(Topics, Topics[order(coefs$Estimate)]))

coefs <- coefs[order(coefs$Estimate),]

qplot(Topics, Estimate, colour=Estimate, size=abs(t.value), data=coefs) + geom_errorbar(width=0.5, aes(ymin=Estimate-Std..Error, ymax=Estimate+Std..Error)) + coord_flip()

predictions <- slda.predict(docs$documents, result$topics, result$model, alpha=1.0, eta=0.1)

#qplot(predictions, fill=factor(gender), xlab="predicted gender", ylab="density", alpha=I(0.5), geom="density") + geom_vline(aes(xintercept=0))+ theme(legend.position="none")

qplot(predictions, fill=factor(gender), xlab="predicted gender", ylab="density", alpha=I(0.5), geom="density") + geom_vline(aes(xintercept=0))+ theme(legend.position="right") +  scale_fill_discrete(name="Gender", labels=c('Female', 'Male'))

predictions

predicted.docsums <- slda.predict.docsums(docs$documents, result$topics, alpha=1.0, eta=0.1)

predicted.proportions <- t(predicted.docsums)/colSums(predicted.docsums)

#qplot(`Topic 1`, `Topic 2`, data = structure(data.frame(predicted.proportions), names = paste("Topic", 1:10)), size = `Topic 3`)

# create train and test partition to test the accuracy of the model 
train_indices <- sample(1:length(docs$documents), length(docs$documents)*0.8)

train_docs <- docs$documents[train_indices]
train_gender <- gender[train_indices]
idx = 1:length(docs$documents)
test_indices = idx[!(idx %in% train_indices)]
test_docs <- docs$documents[test_indices]

result <- slda.em(train_docs, K=num.topics, vocab=docs$vocab, num.e.iterations=10, num.m.iterations=4, alpha=1.0, eta=1.0, train_gender, params, variance=0.25, lambda=1.0, logistic=FALSE, method="sLDA")

predictions <- slda.predict(test_docs, result$topics, result$model, alpha=1.0, eta=0.1)

# set a threshold for classification
actual = as.integer(gender[test_indices])
preds = predictions
preds[predictions > 0] = 1
preds[predictions < 0] = -1
# compute the confusion matrix
cm = as.matrix(table(Actual = actual, Predicted = preds))
# compute accuracy from the confusion matrix
n = sum(cm)
nc = nrow(cm)
diag = diag(cm)
accuracy = sum(diag) / n

sprintf("Accuracy of predictions: %s", accuracy)

# compute demographic parity
fempreds = preds[preds < 0]
malpreds = preds[preds > 0]
genderratio_in_pred = length(malpreds)/(length(malpreds) + length(fempreds))
femactual = actual[actual < 0]
malactual = actual[actual > 0]
genderratio_actual =length(malactual)/(length(femactual)+length(malactual))
dem_parity = genderratio_in_pred / genderratio_actual

sprintf("Ratio of male percentage in prediction and in actuality: %s", dem_parity)

# test on simulated data 
dat_simulated = readLines("~/Downloads/test_docs_slda_20topics.csv")
sim_docs <- lexicalize(dat_simulated, sep=",", lower=TRUE, count=1L, vocab=docs$vocab)


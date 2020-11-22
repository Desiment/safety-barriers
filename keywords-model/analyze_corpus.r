library(tm)
library(NLP)
library(SnowballC)
library(wordcloud)
library(wordcloud2)
library(RColorBrewer)


dic_demo <- NULL
if(!file.exists("dictonary_freq.dic"))
{
    data_path <- "demo.dic"
    stopwords_path <- "stopwords.ru"

    dic_demo <- readLines(data_path)
    stopwords <- readLines(stopwords_path)

    #Use lem instead of stem
    dic_demo <- removeWords(dic_demo, words = stopwords)
    for(i in 0:length(dic_demo)) 
        {dic_demo[i] <- tolower(wordStem(dic_demo[i], language="russian")) }
    dic_demo <- removeWords(dic_demo, words = stopwords)

    #Save
    lapply(dic_demo, write, "dictonary_freq.dic", append=TRUE)
} else
{
   dic_demo <- readLines("dictonary_freq.dic")
}

#Size of unique(dic) is 79870
#Should use Hemming or Lewinstein distance beetwen words O(n^2), to merge same words

#Tables
#pre_frequency  <- table(dic_demo)
#word_frequency <- cbind(names(pre_frequency), as.integer(pre_frequency))

class(dic_demo)
word_cloud <- unlist(dic_demo)

png(wordcloud(word_cloud,min.freq = 3, max.words=1000, random.order=F, colors=brewer.pal(5, "Dark2"), scale=c(20,0.15)), filename="tedt.png")






library(rjson)
library(plyr)
library(dplR)
library(stringr)
library(dplyr)
setwd("C:/Users/heman/OneDrive/Documents/DCMME/WHIN")

Certification_list <- read.csv("Certification list.csv")


#INITIAL ANALYSIS OF TEXT--------------------------------------------------
#extracting json file as list 
result <- fromJSON(file = "json_30www.mw-ind.com.json")
print(result)


# data=c()
# for(i in 1:length(result))
# {
#   data[i] = result[[i]]
# }

#vector of json file
#vector <- as.character(result)

#list of sentences 
text_df <- data_frame(line = names(result), text = as.character(result))

library(tidytext)
list_of_words <- text_df %>% unnest_tokens(word, text)

#removing all stop words 
data("stop_words")
words_without_stopwords <- list_of_words %>% anti_join(stop_words)

#displaying a count of different words 
word_count <- list_of_words %>% count(word, sort = TRUE)
word_count <- words_without_stopwords %>% count(word, sort = TRUE)


#TRYING TO LOCATE ISO CERTIFICATIONS----------------------------------------

words_without_stopwords$word=paste("-",words_without_stopwords$word,"-")
Certification_list$Certifications=paste("-",Certification_list$Certifications,"-")

for(j in Certification_list$Certifications)
{
  print(j)
  data=subset(x = words_without_stopwords,grepl(j,words_without_stopwords$word,ignore.case = T)==TRUE)
print(data)
    }



#TRYING TO FIND WORDS ASSOCIATED WITH PRODUCTS-------------------------------

a=as.data.frame(findAssocs(dtm,pos_frequency$word[i], 0.1))

#TRYING TO FIND WORDS ASSOCIATED WITH EQUIPMENT ------------------------------


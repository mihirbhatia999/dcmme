library(rjson)
library(plyr)
library(dplR)
library(stringr)
library(dplyr)
setwd("W:/pu.data/Desktop/Scrapper_to_use")

#INITIAL ANALYSIS OF TEXT--------------------------------------------------
#extracting json file as list 
result <- fromJSON(file = "example_1.json")
print(result)

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



#TRYING TO FIND WORDS ASSOCIATED WITH PRODUCTS-------------------------------




#TRYING TO FIND WORDS ASSOCIATED WITH EQUIPMENT ------------------------------


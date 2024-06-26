library(rvest)
library(dplyr)
library(lubridate)
library(readr)

crypto_csv_table <- 'Crypto_Automated_Pull.csv'

automated_crypto_pull <- function() {
  tryCatch({
    url <- 'https://coinmarketcap.com/currencies/bitcoin/'
    page <- read_html(url)
    
    crypto_name_tag <- page %>% html_node('.sc-d1ede7e3-0.bEFegK') %>% html_text()
    crypto_price_tag <- page %>% html_node('.sc-d1ede7e3-0.fsQm.base-text') %>% html_text()
    
    if (!is.na(crypto_name_tag) & !is.na(crypto_price_tag)) {
      crypto_name <- gsub('price|\\xa0', '', crypto_name_tag)
      crypto_price <- as.numeric(gsub('[\\$,]', '', crypto_price_tag))
      
      date_time <- now()
      data <- tibble(Crypto_Name = crypto_name, Price = crypto_price, TimeStamp = date_time)
      
      if (file.exists(crypto_csv_table)) {
        write_csv(data, crypto_csv_table, append = TRUE)
      } else {
        write_csv(data, crypto_csv_table)
      }
      
      print(data)
    } else {
      print("Failed to find the required tags on the page.")
    }
  }, error = function(e) {
    print(paste("An error occurred:", e))
  })
}

while (TRUE) {
  automated_crypto_pull()
  Sys.sleep(5)
}

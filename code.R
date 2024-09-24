# Load necessary libraries ------------------------------------------------

library(RSelenium)   # For using Selenium to automate web browser actions
library(tidyverse)   # For data manipulation (ggplot2, dplyr, etc.)
library(netstat)     # For network statistics and port availability
library(httr)        # For working with HTTP (web scraping, APIs, etc.)
library(wdman)       # For managing Selenium WebDrivers
library(rvest)       # For web scraping and parsing HTML content

# Check and install wdman if not already installed ------------------------

if (!requireNamespace("wdman", quietly = TRUE)) {
  install.packages("wdman")  # Install wdman if not present
}

# Start the Selenium server -----------------------------------------------

# Run the Selenium server and return the command to be used, if needed.
wdman::selenium(retcommand = TRUE, check = FALSE) 
wdman::selenium(retcommand = TRUE, check = FALSE)

# Alternatively, just start Selenium server without returning a command
wdman::selenium()

# Start a Remote Driver (Selenium Client) ---------------------------------

# Create a Selenium remote driver object to connect to the server running on localhost with Chrome
remDr <- remoteDriver(remoteServerAddr = "localhost", browserName = "chrome")

# Attempt to open the browser
remDr$open()

# Specify a different port if needed --------------------------------------

# Connect to the Selenium server running on port 4567 (change port as needed)
remDr <- remoteDriver(remoteServerAddr = "localhost", port = 4567L, browserName = "chrome")

# Open the browser again
remDr$open()

# Navigate to the target webpage ------------------------------------------

# Direct the browser to navigate to the Sotheby's auction webpage
remDr$navigate("https://www.sothebys.com/en/auctions/2012/latin-american-art-n08862.html")

# Scrape the webpage ------------------------------------------------------

# Get the raw HTML source code of the webpage
page_source <- remDr$getPageSource()[[1]] 

# Parse the HTML content using rvest for further manipulation
page_html <- read_html(page_source)
page_html

# Select all artwork items listed on the webpage --------------------------

# Extract the artwork elements based on the specific HTML structure (list items)
artworks <- page_html %>% html_nodes(xpath = '//li[@class="AuctionsModule-results-item"]')
artworks

# Extract information from the artwork items -----------------------------

# Get the author/artist's name for each artwork
author <- artworks %>% html_node(xpath = './/div[@class="title "]/a') %>% html_text(trim = TRUE)
author

# Get the title of the artwork
title <- artworks %>% html_node(xpath = './/div[@class="description"]') %>% html_text(trim = TRUE)
title

# Get the estimated price range of the artwork
estimate_text <- artworks %>% html_node(xpath = './/div[@class="estimate"]') %>% html_text(trim = TRUE)
estimate_text

# Clean and manipulate the data -------------------------------------------

# Create a tibble (dataframe) and clean the estimate_text column
result <- tibble(estimate_text) %>%
  mutate(values = str_remove_all(estimate_text, "Estimate: | USD"),  # Remove 'Estimate:' and 'USD'
         values = str_remove_all(values, ",")) %>%  # Remove commas from the text
  separate(values, into = c("before", "after"), sep = " – ") %>%  # Split the price range into 'before' and 'after'
  mutate(across(c(before, after), as.numeric))  # Convert the text values to numeric

# Extract the minimum and maximum estimates
min_estimate <- result$before
max_estimate <- result$after

# Print the extracted estimates to the console
print(min_estimate)
print(max_estimate)

# Interact with elements on the webpage -----------------------------------

# Find and click the "Log In" button on the webpage
log_in_button <- remDr$findElement(using = "xpath", '//a[@data-text-content="Log In"]')
log_in_button$clickElement()

# Find the email and password fields --------------------------------------

# Locate the email field on the login page
email_field <- remDr$findElement(using = "xpath", '//input[@placeholder="Email address"]')

# Locate the password field
password_field <- remDr$findElement(using = "xpath", '//input[@placeholder="Password"]')

# Enter credentials -------------------------------------------------------

# Send the email address to the email input field
email_field$sendKeysToElement(list("r.workshop.umd@gmail.com"))

# Send the password to the password input field
password_field$sendKeysToElement(list("Workshop123"))

# Click the login button --------------------------------------------------

# Locate and click the login button to attempt login
login_button <- remDr$findElement(using = "id", 'login-button-id')
login_button$clickElement()

# Re-navigate to the auction webpage --------------------------------------

# Navigate back to the auction page after login
remDr$navigate("https://www.sothebys.com/en/auctions/2012/latin-american-art-n08862.html")

# Pause the script for 5 seconds to allow the page to load fully
Sys.sleep(5)

# Extract sold prices from the webpage ------------------------------------

# Find and extract the sold price information from the artwork items
sold_price <- artworks %>% html_node(xpath = './/div[@class="sold"]') %>% html_text(trim = TRUE) %>% str_replace("Lot Sold: ", "")
sold_price

# Create a dataframe with the collected artwork data ----------------------

# Combine all the collected data into a structured dataframe
artworks_info <- data.frame(
  Author = author,
  Title = title,
  Min_Estimate = min_estimate,
  Max_Estimate = max_estimate,
  Sold_Price = sold_price,
  stringsAsFactors = FALSE  # Ensure that strings are not converted to factors
)
artworks_info

# Close the browser session -----------------------------------------------

# Close the Selenium browser session
remDr$close()


## Scrape multiple pages with for loop:

remDr <- remoteDriver(remoteServerAddr = "localhost", port = 4567L, browserName = "chrome")

# Intenta abrir el navegador
remDr$open()

remDr$navigate("https://www.sothebys.com/en/auctions/2012/latin-american-art-n08862.html")

# Columnas del dataframe
columns <- c("Author", "Title", "Min Estimate", "Max Estimate", "Sold Price", 
             "Auction Title", "Auction Date", "Sale Total", "Sale Number", 
             "Lots Count", "Web", "Web Number", "Code", "Year")
df_empty_total <- data.frame(matrix(ncol = length(columns), nrow = 0),  stringsAsFactors = FALSE)
df_empty_total[] <- lapply(df_empty_total, as.character)

colnames(df_empty_total) <- columns

# Loop para procesar cada página
for (web in paginas) {
  print(paste("Procesando:", web))
  
  remDr$navigate(web)
  Sys.sleep(5)
  
  # Intentar obtener el número de la última página
  tryCatch({
    last_page_number <- remDr$findElement(using = "xpath", '//a[@class="with-border "][last()]')$getElementText() %>% as.integer()
  }, error = function(e) {
    print(paste("Error to obtain number of pages:", e$message))
    last_page_number <- 1
  })
  
  for (i in 1:last_page_number) {
    print(paste("Page:", i, "from", last_page_number))
    
    # Navegar a la página correspondiente
    remDr$navigate(paste0(web, "?p=", i))
    Sys.sleep(2)
    
    # Intentar verificar el mensaje "Log in to view sale total"
    tryCatch({
      sale_total_message <- remDr$findElement(using = "xpath", '//div[contains(text(), "Log in to view sale total")]')
      if (!is.null(sale_total_message)) {
        print("Message 'Log in to view sale total' found, refresh the webpage...")
        remDr$refresh()
        Sys.sleep(5)
      }
    }, error = function(e) {
      print("Couldn't be found the message 'Log in to view sale total'")
    })
    
    # Extraer la información de las obras de arte
    artworks_info <- list()
    
    # Obtener los elementos de arte en la página
    tryCatch({
      page_source <- remDr$getPageSource()[[1]]
      page_html <- read_html(page_source)
      artworks <- page_html %>% html_nodes(xpath = '//li[@class="AuctionsModule-results-item"]')
      
      author <- artworks %>% html_node(xpath = './/div[@class="title "]/a') %>% html_text(trim = TRUE)
      title <- artworks %>% html_node(xpath = './/div[@class="description"]') %>% html_text(trim = TRUE)
      estimate_text <- artworks %>% html_node(xpath = './/div[@class="estimate"]') %>% html_text(trim = TRUE)
      estimates <- str_replace_all(estimate_text, "Estimate: |USD", "") %>% str_split(" – ") %>% .[[1]]
      min_estimate <- ifelse(length(estimates) >= 1, estimates[1], NA)
      max_estimate <- ifelse(length(estimates) == 2, estimates[2], NA)
      sold_price <- artworks %>% html_node(xpath = './/div[@class="sold"]') %>% html_text(trim = TRUE) %>% str_replace("Lot Sold: ", "")
      
      auction_title <- page_html %>% html_node(xpath = '//div[@class="AuctionsModule-auction-title"]') %>% html_text(trim = TRUE)
      auction_date <- page_html %>% html_node(xpath = '//div[@class="AuctionsModule-auction-info"]') %>% html_text(trim = TRUE)
      sale_total <- page_html %>% html_node(xpath = '//div[@class="AuctionsModule-auction-info-totalPrice"]') %>% html_text(trim = TRUE)
      sale_number <- page_html %>% html_node(xpath = '//div[@class="AuctionsModule-auction-info-saleNumber"]') %>% html_text(trim = TRUE)
      lots_count <- page_html %>% html_node(xpath = '//div[@class="AuctionsModule-lotsCount"]') %>% html_text(trim = TRUE)
      
      artworks_info <- data.frame(
        Author = author,
        Title = title,
        Min_Estimate = min_estimate,
        Max_Estimate = max_estimate,
        Sold_Price = sold_price,
        stringsAsFactors = FALSE
      )
      artworks_info$Auction_Title = auction_title
      artworks_info$Auction_Date = auction_date
      artworks_info$Sale_Total = sale_total
      artworks_info$Sale_Number = sale_number
      artworks_info$Lots_Count = lots_count
      artworks_info$Web = web
      artworks_info$Web_Number = i
      
    }, error = function(e) {
      print(paste("Error scraping data:", e$message))
    })
    
    df_empty_total <- bind_rows(df_empty_total, artworks_info)
    
    print(paste("Data extract from the page", i, " from", web))
  }
}

# Guardar el dataframe en Excel
write.xlsx(df_empty_total, "dataframe_auctions_LatinAmerica.xlsx")
remDr$close()
# Load packages needed for exercise
library(readr)
library(dplyr)
library(ggplot2)
library(purrr)

# Import the dataset we will be working with
forest_fires <- read_csv('forestfires.csv')

# Update data types for the month, day so they are in an order that makes more sense
forest_fires <- forest_fires %>%
  mutate(month = factor(month, levels = c('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'))) %>%
  mutate(day = factor(day, levels = c('sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat')))

# Analyze the number of fires by month
fires_by_month <- forest_fires %>%
  group_by(month) %>%
  summarize(total_fires = n())

ggplot(data = fires_by_month) +
  aes(x = month, y = total_fires) +
  geom_bar(stat = 'identity') +
  theme(panel.background = element_rect(fill = 'white'))

# Analyze the number of fires by day
fires_by_day_of_week <- forest_fires %>%
  group_by(day) %>%
  summarize(total_fires = n())

ggplot(data = fires_by_day_of_week) +
  aes(x = day, y = total_fires) +
  geom_bar(stat = 'identity') +
  theme(panel.background = element_rect(fill = 'white'))

# Function to generate boxplots for dataset
create_boxplots <- function(x, y) {
  ggplot(data = forest_fires) +
    aes_string(x = x, y = y) +
    geom_boxplot() +
    theme(panel.background = element_rect(fill = 'white'))
}

# Get variable names
x_var_month <- names(forest_fires)[3]
x_var_day <- names(forest_fires)[4]
y_var <- names(forest_fires)[5:12]

# Map the function to the appropriate variables
month_box <- map2(x_var_month, y_var, create_boxplots)
day_box <- map2(x_var_day, y_var, create_boxplots)

month_box
day_box


x_var <- names(forest_fires)[5:12]
y_var_area <- names(forest_fires)[13]

create_scatterplots <- function(x, y) {
  ggplot(data = forest_fires) +
    aes_string(x = x, y = y) +
    geom_point() +
    theme(panel.background = element_rect(fill = 'white'))
}

area_scatter <- map2(x_var, y_var_area, create_scatterplots)
area_scatter
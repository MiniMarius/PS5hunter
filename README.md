# PS5 Hunter

## Overview

PS5 Hunter is a Python-based web scraping project aimed at providing a powerful tool for obtaining stock information of online products. The project was developed with the intention of helping users track the availability of PS5s and other high-demand products, making it easier for them to purchase these items before they sell out.

The PS5 Hunter project uses the BeautifulSoup library to scrape web pages and obtain relevant stock information, such as product availability, price, and other details. This project includes a Django-based backend with a React frontend that makes it easy for users to execute the web scraping process and obtain the desired information.

## Features

The PS5 Hunter project includes/will include the following features:

- Ability to scrape multiple web pages simultaneously to obtain real-time stock information for PS5s and other high-demand products.
- Customizable search parameters that allow users to filter results based on specific needs.
- User-friendly web interface that makes it easy to execute the web scraping process and obtain the desired information.
- Support for email notifications that can alert users when a product becomes available for purchase.
- User-friendly documentation that provides clear instructions on how to use the tool.

## Requirements

The PS5 Hunter project requires the following software and libraries to be installed:

- Python 3.6 or higher
- Django 3.0 or higher
- BeautifulSoup4
- Requests

## Usage

In the near future, this project will be deployed for everyone to use. In this stage, to use the PS5 Hunter project, follow these steps:

1. Clone the project repository to your local machine.
2. Install the required software and libraries listed above.
3. Open a terminal window and navigate to the project directory.
4. Run the following command to start the Django server:

    `python manage.py runserver`

5. Open a web browser and navigate to the local server address provided by Django.
6. Follow the on-screen prompts to enter your search parameters and obtain the desired stock information.

## Frontend

The frontend code for the PS5 Hunter project is hosted in a separate repository at [https://github.com/MiniMarius/PS5hunter_frontend](https://github.com/MiniMarius/PS5hunter_frontend). 

## Limitations

The PS5 Hunter project has the following limitations:

- The tool is dependent on the structure and layout of the web pages being scraped. It cannot handle websites that utilize AJAX pagination and other kinds of infinite scrolling mechanisms.  It also relies on the information stored in the Website objects being correct. If the layout of a particular web page changes, the tool may not be able to obtain the desired information.
- The tool is only as accurate as the information provided on the web pages being scraped. If a web page lists inaccurate or outdated information, the tool may provide incorrect results.


# Crazy Days and Nights Lawsuit

~~You can view the final output of this project at [Crazy Days and Nights Lawsuit](https://www.crazydaysandnightslawsuit.net)~~
Project is now defunct. It was availale on "https://www.crazydaysandnightslawsuit.net" until end of 2023.

## Purpose

The purpose of this project was to test the capabilities of GPT-3.5 Turbo. The tasks before it included the ability to
- clone the blog "Crazy Days and Nights",
- provide numerical analysis about the blog, and
- provide updates on the latest legal challenges faced by the blog.

## Project Overview

This project is a fully developed and comprehensive, data-driven web service app. It was built using **Flask**, **HTML**, **CSS**, **JavaScript**, and **MySQL**, focusing on a real-world lawsuit investigation. 

## Infrastructure 

A robust data infrastructure was established with a self-hosted MySQL database and two AWS EC2 instances - one hosting the application and master database, and the other serving as a replica for increased data reliability and performance.

## Task Automation

Designed and executed a scheduled task using CRON jobs, which performs daily data scraping using Python’s Beautiful Soup and facilitates automated backup of the database via mysqldump exports and imports, enhancing data safety and integrity.

## Domain and Security

Configured AWS Route 53 for domain purchase and forwarding, and set up HTTPS for secure communication. 

## Database Integration

Integrated the database with the web application to display real-time data to users, applying best practices for data security by using a MySQL user with limited privileges. 

## Version Control

Utilized Git for effective version control throughout the project.

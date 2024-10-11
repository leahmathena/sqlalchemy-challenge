# SQLAlchemy Challenge - Climate Analysis and Flask API

## Overview
This project involves analyzing climate data from Honolulu, Hawaii, to aid in trip planning. Using Python, SQLAlchemy, and Flask, I explored and visualized the climate data while developing an API to provide access to the analysis results.

## Project Components

### Data Analysis
- **Database Connection:** Established a connection to an SQLite database containing climate data using SQLAlchemy.
- **Data Exploration:**
  - Reflected database tables into Python classes for easy querying.
  - Conducted a precipitation analysis by retrieving and visualizing the last 12 months of precipitation data.
  - Analyzed station data to find the most active stations and summarized temperature statistics.

### Visualization
- Utilized Pandas and Matplotlib to create visual representations of the precipitation data and temperature observations, including:
  - Time series plots of precipitation.
  - Histograms of temperature observations for the most active station.

### Flask API Development
- Developed a Flask application to create endpoints for accessing climate data:
  - **Home Route:** Displays available API routes.
  - **Precipitation Route:** Returns JSON data for the last 12 months of precipitation.
  - **Stations Route:** Lists all weather stations.
  - **Temperature Observations Route:** Provides temperature data for the most active station.
  - **Dynamic Routes:** Allows users to query temperature statistics over specified date ranges.


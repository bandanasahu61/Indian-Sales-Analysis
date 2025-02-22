import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from datetime import datetime, timedelta
import locale

# First set the style using seaborn directly
sns.set_theme()
# Set a more modern style
plt.style.use('seaborn-v0_8-darkgrid')  # Using the updated style name

class IndianSalesAnalysis:
    def __init__(self):
        self.categories = [
            'Electronics', 'Clothing', 'Groceries', 
            'Home Appliances', 'Mobile Phones',
            'Furniture', 'Books', 'Sports Equipment'
        ]
        
        self.cities = [
            'Mumbai', 'Delhi', 'Bangalore', 
            'Chennai', 'Kolkata', 'Hyderabad',
            'Pune', 'Ahmedabad'
        ]

    def format_currency(self, amount):
        """Format amount in Indian currency format"""
        try:
            return f"₹{amount:,.2f}"
        except:
            return amount

    def generate_sales_data(self, num_records=1000):
        """Generate sample sales data with Indian context"""
        np.random.seed(42)
        
        start_date = datetime(2023, 1, 1)
        dates = [start_date + timedelta(days=x) for x in range(num_records)]
        
        data = {
            'Date': dates,
            'Category': [random.choice(self.categories) for _ in range(num_records)],
            'City': [random.choice(self.cities) for _ in range(num_records)],
            'Sales_Amount': np.random.uniform(1000, 100000, num_records).round(2),
            'Units_Sold': np.random.randint(1, 50, num_records),
            'Customer_Rating': np.random.uniform(3.0, 5.0, num_records).round(1),
            'Profit_Margin': np.random.uniform(0.1, 0.4, num_records).round(3),
            'GST_Amount': np.random.uniform(100, 10000, num_records).round(2)
        }
        
        df = pd.DataFrame(data)
        df = df.sort_values('Date')
        return df.reset_index(drop=True)

    def create_visualizations(self, df):
        """Create comprehensive visualizations"""
        
        # Set color palette
        colors = sns.color_palette("husl", 8)
        
        # Create plots directory
        import os
        if not os.path.exists('indian_sales_plots'):
            os.makedirs('indian_sales_plots')

        # 1. Monthly Sales Trend with Indian Currency
        plt.figure(figsize=(15, 7))
        monthly_sales = df.groupby(df['Date'].dt.strftime('%Y-%m'))['Sales_Amount'].sum()
        ax = monthly_sales.plot(kind='line', marker='o', linewidth=2, markersize=8, color=colors[0])
        plt.title('Monthly Sales Trend (2023-2025)', fontsize=14, pad=20)
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Total Sales (₹)', fontsize=12)
        
        # Format y-axis in Indian currency format (lakhs)
        def format_in_lakhs(x, p):
            return f'₹{x/100000:.1f}L'
        
        ax.yaxis.set_major_formatter(plt.FuncFormatter(format_in_lakhs))
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('indian_sales_plots/monthly_sales_trend.png', dpi=300, bbox_inches='tight')
        plt.close()

        # 2. Category-wise Sales Distribution
        plt.figure(figsize=(12, 6))
        category_sales = df.groupby('Category')['Sales_Amount'].sum().sort_values(ascending=False)
        ax = category_sales.plot(kind='bar', color=colors[1])
        plt.title('Sales Distribution by Category', fontsize=14, pad=20)
        plt.xlabel('Category', fontsize=12)
        plt.ylabel('Total Sales (₹)', fontsize=12)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(format_in_lakhs))
        plt.xticks(rotation=45)
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('indian_sales_plots/category_sales.png', dpi=300, bbox_inches='tight')
        plt.close()

        # 3. City-wise Performance (Pie Chart)
        plt.figure(figsize=(12, 8))
        city_sales = df.groupby('City')['Sales_Amount'].sum()
        plt.pie(city_sales, labels=city_sales.index, autopct='%1.1f%%', 
                startangle=90, pctdistance=0.85, colors=colors)
        centre_circle = plt.Circle((0,0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.title('Sales Distribution by City', fontsize=14, pad=20)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('indian_sales_plots/city_sales_pie.png', dpi=300, bbox_inches='tight')
        plt.close()

        # 4. Correlation Heatmap
        plt.figure(figsize=(10, 8))
        numeric_cols = ['Sales_Amount', 'Units_Sold', 'Customer_Rating', 
                       'Profit_Margin', 'GST_Amount']
        correlation = df[numeric_cols].corr()
        sns.heatmap(correlation, annot=True, cmap='RdYlBu', center=0)
        plt.title('Correlation Heatmap', fontsize=14, pad=20)
        plt.tight_layout()
        plt.savefig('indian_sales_plots/correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()

        # 5. Daily Sales Pattern
        plt.figure(figsize=(15, 7))
        df['DayOfWeek'] = df['Date'].dt.day_name()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                    'Friday', 'Saturday', 'Sunday']
        daily_sales = df.groupby('DayOfWeek')['Sales_Amount'].mean()
        daily_sales = daily_sales.reindex(day_order)
        ax = daily_sales.plot(kind='bar', color=colors[4])
        plt.title('Average Daily Sales Pattern', fontsize=14, pad=20)
        plt.xlabel('Day of Week', fontsize=12)
        plt.ylabel('Average Sales (₹)', fontsize=12)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(format_in_lakhs))
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('indian_sales_plots/daily_sales_pattern.png', dpi=300, bbox_inches='tight')
        plt.close()

        # 6. Box Plot of Sales by Category
        plt.figure(figsize=(15, 7))
        sns.boxplot(x='Category', y='Sales_Amount', data=df, palette=colors)
        plt.title('Sales Distribution by Category (Box Plot)', fontsize=14, pad=20)
        plt.xticks(rotation=45)
        plt.ylabel('Sales Amount (₹)')
        plt.tight_layout()
        plt.savefig('indian_sales_plots/category_sales_boxplot.png', dpi=300, bbox_inches='tight')
        plt.close()

    def generate_summary_report(self, df):
        """Generate comprehensive summary report with Indian currency format"""
        
        report = {
            'total_sales': self.format_currency(df['Sales_Amount'].sum()),
            'average_sale': self.format_currency(df['Sales_Amount'].mean()),
            'total_units': f"{df['Units_Sold'].sum():,}",
            'avg_rating': f"{df['Customer_Rating'].mean():.2f}/5.0",
            'total_gst': self.format_currency(df['GST_Amount'].sum()),
            'avg_profit_margin': f"{df['Profit_Margin'].mean():.1%}",
            'best_category': df.groupby('Category')['Sales_Amount'].sum().idxmax(),
            'best_city': df.groupby('City')['Sales_Amount'].sum().idxmax(),
            'total_transactions': f"{len(df):,}"
        }
        
        # Monthly analysis
        df['Month'] = df['Date'].dt.strftime('%B %Y')
        best_month = df.groupby('Month')['Sales_Amount'].sum().idxmax()
        report['best_month'] = best_month
        
        return report

    def save_data(self, df, filename='indian_sales_data.csv'):
        """Save generated data to CSV"""
        try:
            df.to_csv(filename, index=False)
            print(f"\nData successfully saved to {filename}")
        except Exception as e:
            print(f"Error saving file: {e}")

def main():
    # Initialize the analysis class
    analysis = IndianSalesAnalysis()
    
    # Generate sample data
    print("Generating Indian sales data...")
    sales_df = analysis.generate_sales_data()
    
    # Save data to CSV
    analysis.save_data(sales_df)
    
    # Create visualizations
    print("\nCreating visualizations...")
    analysis.create_visualizations(sales_df)
    
    # Generate and print summary report
    print("\nGenerating summary report...")
    report = analysis.generate_summary_report(sales_df)
    
    # Print detailed summary
    print("\n=== Indian Sales Analysis Summary ===")
    print(f"\nTotal Sales: {report['total_sales']}")
    print(f"Average Sale per Transaction: {report['average_sale']}")
    print(f"Total Units Sold: {report['total_units']}")
    print(f"Total GST Collected: {report['total_gst']}")
    print(f"Average Customer Rating: {report['avg_rating']}")
    print(f"Average Profit Margin: {report['avg_profit_margin']}")
    print(f"Best Performing Category: {report['best_category']}")
    print(f"Best Performing City: {report['best_city']}")
    print(f"Best Performing Month: {report['best_month']}")
    print(f"Total Number of Transactions: {report['total_transactions']}")
    
    print("\nVisualization files have been saved in 'indian_sales_plots' directory:")
    print("- monthly_sales_trend.png")
    print("- category_sales.png")
    print("- city_sales_pie.png")
    print("- correlation_heatmap.png")
    print("- daily_sales_pattern.png")
    print("- category_sales_boxplot.png")

if __name__ == "__main__":
    main()

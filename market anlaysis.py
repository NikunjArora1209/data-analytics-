import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Load dataset
df = pd.read_csv("cleaned_customer_purchase_history.csv")

# Create basket table
basket = df.pivot_table(index='CustomerID',
                        columns='Product',
                        values='Quantity',
                        aggfunc='sum',
                        fill_value=0)

# Convert to binary
basket = (basket > 0).astype(int)

# Frequent itemsets
frequent_items = apriori(basket, min_support=0.01, use_colnames=True)

# Association rules
rules = association_rules(frequent_items, metric="confidence", min_threshold=0.1)

# Convert sets to text
rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))

# Product-wise analysis
products = basket.columns

print("\nProduct Based Insights:\n")

for product in products:
    
    users = basket[product].sum()
    print(f"\nProduct: {product}")
    print(f"Total users who bought {product}: {users}")
    
    related = rules[rules['antecedents'].str.contains(product)]
    
    if not related.empty:
        print("Customers also bought:")
        print(related[['consequents','confidence','lift']])
    else:
        print("No strong association found")
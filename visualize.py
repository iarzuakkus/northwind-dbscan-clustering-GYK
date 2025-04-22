import matplotlib.pyplot as plt
from database_connect import cutomer_segmentation, product_segmentation, supplier_segmentation, country_segmentation
from model import apply_dbscan


def plot_dynamic_segmentation(df, x_col, y_col, title=None, color_map='plasma'):
    if 'cluster' not in df.columns:
        raise ValueError("DataFrame içinde 'cluster' sütunu yok. DBSCAN sonrası dataframe bekleniyor.")
    
    if title is None:
        title = f"{x_col.replace('_', ' ').title()} vs {y_col.replace('_', ' ').title()}"

    plt.figure(figsize=(10, 6))
    plt.scatter(
        df[x_col], 
        df[y_col], 
        c=df['cluster'], 
        cmap=color_map, 
        s=60
    )
    plt.xlabel(x_col.replace('_', ' ').title())
    plt.ylabel(y_col.replace('_', ' ').title())
    plt.title(title)
    plt.grid(True)
    plt.colorbar(label='Küme No')
    plt.show()
if __name__ ==  '__main__':
    
    plot_dynamic_segmentation(apply_dbscan(cutomer_segmentation()), x_col="total_orders", y_col="total_spent")
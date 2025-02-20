from typing import List, Optional, Dict
from providers.firebase import products_collection

def get_all_products() -> List[dict]:
    try:
        products = products_collection.stream()
        product_list = []
        for doc in products:
            product = doc.to_dict()
            product['id'] = doc.id
            product_list.append(product)
        return product_list
    except Exception as e:
        raise e

async def create_product(product_data: Dict) -> Dict:
    try:
        new_product_ref = products_collection.document()
        new_product_ref.set(product_data)
        new_product = new_product_ref.get().to_dict()
        new_product['id'] = new_product_ref.id
        return new_product
    except Exception as e:
        raise e

async def update_product(product_id: str, product_data) -> Optional[dict]:
    try:
        product_ref = products_collection.document(product_id)
        product = product_ref.get()
        if not product.exists:
            return None
        update_data = product_data.dict(exclude_unset=True)
        product_ref.update(update_data)
        updated_product = product_ref.get().to_dict()
        updated_product['id'] = product_id
        return updated_product
    except Exception as e:
        raise e

async def delete_product(product_id: str) -> bool:
    try:
        product_ref = products_collection.document(product_id)
        product = product_ref.get()
        if not product.exists:
            return False
        product_ref.delete()
        return True
    except Exception as e:
        raise e
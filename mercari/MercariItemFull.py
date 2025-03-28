# some endpoints use similar keys but different case, bidDeadline vs bid_deadline
def get_from_kwargs(kwargs, *keys, default=""):
    for key in keys:
        if key in kwargs:
            return kwargs[key]
    return default

class Printable:
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())})"

    def __str__(self, level=0):
        indent = '\t' * level
        items = []
        for k, v in self.__dict__.items():
            if isinstance(v, Printable):
                items.append(f"{indent}\"{k}\": {v.__str__(level + 1)}")
            elif isinstance(v, str):
                items.append(f"{indent}\"{k}\": \"{v}\"")
            elif isinstance(v, list) and all(isinstance(i, Printable) for i in v):
                if len(v) == 0:
                    items.append(f"{indent}\"{k}\": []")
                else:
                    nested_items = f", ".join(i.__str__(level + 2) for i in v)
                    items.append(f"{indent}\"{k}\": [ {nested_items}\n{indent}\t]")
            else:
                items.append(f"{indent}\"{k}\": {v}")
        return '{\n\t' + ',\n\t'.join(items) + f'\n{indent}}}'

class Ratings(Printable):
    good: int
    normal: int
    bad: int

    def __init__(self, *args, **kwargs):
        self.good = kwargs['good']
        self.normal = kwargs['normal']
        self.bad = kwargs['bad']

class ConvertedPrice(Printable):
    price: int
    currency_code: str
    rate_updated: int

    def __init__(self, *args, **kwargs):
        self.price = kwargs['price']
        self.currency_code = kwargs['currency_code']
        self.rate_updated = kwargs['rate_updated']

class Seller(Printable):
    id: str
    name: str
    photo_url: str
    photo_thumbnail_url: str
    created: int
    num_sell_items: int
    ratings: Ratings
    num_ratings: int
    score: int
    is_official: bool
    quick_shipper: bool
    is_followable: bool
    is_blocked: bool
    star_rating_score: int

    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.photo_url = kwargs['photo_url']
        self.photo_thumbnail_url = kwargs['photo_thumbnail_url']
        self.created = kwargs['created']
        self.num_sell_items = kwargs['num_sell_items']
        self.ratings = Ratings(**kwargs['ratings'])
        self.num_ratings = kwargs['num_ratings']
        self.score = kwargs['score']
        self.is_official = kwargs['is_official']
        self.quick_shipper = kwargs['quick_shipper']
        self.is_followable = kwargs['is_followable']
        self.is_blocked = kwargs['is_blocked']
        self.star_rating_score = kwargs['star_rating_score']

class ItemCategory(Printable):
    id: str
    name: str
    display_order: int
    parent_category_id: int
    parent_category_name: str
    root_category_id: int
    root_category_name: str
    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.display_order = kwargs['display_order']
        self.parent_category_id = kwargs['parent_category_id']
        self.parent_category_name = kwargs['parent_category_name']
        self.root_category_id = kwargs['root_category_id']
        self.root_category_name = kwargs['root_category_name']

class ItemCategoryNTiers(ItemCategory):
    brand_group_id: int = 0

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        if 'brand_group_id' in kwargs:
          self.brand_group_id = kwargs['brand_group_id']

class ParentCategoryNTier(Printable):
    id: str
    name: str
    display_order: int

    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.display_order = kwargs['display_order']

class ItemCondition(Printable):
    id: str
    name: str

    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']

class ShippingPayer(Printable):
    
    id: str
    name: str
    code: str

    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.code = kwargs['code']

class ShippingMethod(Printable):
    id: str
    name: str
    is_deprecated: bool

    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.is_deprecated = kwargs['is_deprecated']

class ShippingFromArea(Printable):
    id: str
    name: str

    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']

class ShippingDuration(Printable):
    id: str
    name: str
    min_days: int
    max_days: int

    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.min_days = kwargs['min_days']
        self.max_days = kwargs['max_days']

class ShippingClass(Printable):
    id: str
    fee: int
    icon_id: int
    pickup_fee: int
    shipping_fee: int
    total_fee: int
    is_pickup: bool

    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.fee = kwargs['fee']
        self.icon_id = kwargs['icon_id']
        self.pickup_fee = kwargs['pickup_fee']
        self.shipping_fee = kwargs['shipping_fee']
        self.total_fee = kwargs['total_fee']
        self.is_pickup = kwargs['is_pickup']
    
class ItemAttributeValue(Printable):
    id: str
    text: str

    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.text = kwargs['text']

class ItemAttribute(Printable):
    id: str
    text: str
    values: list[ItemAttributeValue]
    deep_facet_filterable: bool
    show_on_ui: bool

    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.text = kwargs['text']
        self.values = [ItemAttributeValue(**value) for value in kwargs['values']]
        self.deep_facet_filterable = kwargs['deep_facet_filterable']
        self.show_on_ui = kwargs['show_on_ui']

class Color(Printable):
    id: str
    name: str
    rgb: str

    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.rgb = kwargs['rgb']

class ItemAuction(Printable):
    id: str
    bid_deadline: str
    total_bid: str
    highest_bid: str

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id', "")
        self.bid_deadline = get_from_kwargs(kwargs, 'bid_deadline', 'bidDeadline', 'expected_end_time')
        self.total_bid = get_from_kwargs(kwargs, 'totalBid', 'total_bids', default="0") # yes, one has an 's'. intentional
        self.highest_bid = get_from_kwargs(kwargs, 'highest_bid', 'highestBid', default="0")

class Item(Printable):
    id: str
    productURL: str
    seller: Seller
    converted_price: ConvertedPrice
    status: str
    name: str
    price: int
    description: str
    photos: list[str]
    photo_paths: list[str]
    thumbnails: list[str]
    item_category: ItemCategory
    item_category_ntiers: ItemCategoryNTiers
    parent_categories_ntiers: list[ParentCategoryNTier]
    item_condition: ItemCondition
    colors: list[Color]
    shipping_payer: ShippingPayer
    shipping_method: ShippingMethod
    shipping_from_area: ShippingFromArea
    shipping_duration: ShippingDuration
    shipping_class: ShippingClass
    num_likes: int
    num_comments: int
    registered_prices_count: int
    comments: list[str] # this is empty in test data, find out what it is
    updated: int
    created: int
    pager_id: str
    liked: bool
    checksum: str
    is_dynamic_shipping_fee: bool
    application_attributes: dict # this is empty in test data, find out what it is
    is_shop_item: str
    hash_tags: list[str] # this is empty in test data, find out what it is
    is_anonymous_shipping: bool
    is_web_visible: bool
    is_offerable: bool
    is_organizational_user: bool
    organizational_user_status: str
    is_stock_item: bool
    is_cancelable: bool
    shipped_by_worker: bool
    additional_services: list[str] # this is empty in test data, find out what it is
    has_additional_service: bool
    has_like_list: bool
    is_offerable_v2: bool
    item_attributes: list[ItemAttribute]
    is_dismissed: bool
    photo_descriptions: list[str]
    meta_title: str
    meta_subtitle: str
    auction: ItemAuction = None # this is optional, only present if the item is an auction



    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        # self.productURL = kwargs['productURL']
        self.seller = Seller(**kwargs['seller'])
        self.converted_price = ConvertedPrice(**kwargs['converted_price'])
        self.status = kwargs['status']
        self.name = kwargs['name']
        self.price = kwargs['price']
        self.description = kwargs['description']
        self.photos = kwargs['photos']
        self.photo_paths = kwargs['photo_paths']
        self.thumbnails = kwargs['thumbnails']
        self.item_category = ItemCategory(**kwargs['item_category'])
        self.item_category_ntiers = ItemCategoryNTiers(**kwargs['item_category_ntiers'])
        self.parent_categories_ntiers = [ParentCategoryNTier(**parent) for parent in kwargs['parent_categories_ntiers']]
        self.item_condition = ItemCondition(**kwargs['item_condition'])
        self.colors = [Color(**color) for color in kwargs['colors']] if 'colors' in kwargs else []
        self.shipping_payer = ShippingPayer(**kwargs['shipping_payer'])
        self.shipping_method = ShippingMethod(**kwargs['shipping_method'])
        self.shipping_from_area = ShippingFromArea(**kwargs['shipping_from_area'])
        self.shipping_duration = ShippingDuration(**kwargs['shipping_duration'])
        self.shipping_class = ShippingClass(**kwargs['shipping_class'])
        self.num_likes = kwargs['num_likes']
        self.num_comments = kwargs['num_comments']
        self.registered_prices_count = kwargs['registered_prices_count']
        # self.comments = kwargs['comments']
        self.comments = []
        self.updated = kwargs['updated']
        self.created = kwargs['created']
        self.pager_id = kwargs['pager_id']
        self.liked = kwargs['liked']
        self.checksum = kwargs['checksum']
        self.is_dynamic_shipping_fee = kwargs['is_dynamic_shipping_fee']
        # self.application_attributes = kwargs['application_attributes']
        self.application_attributes = {}
        self.is_shop_item = kwargs['is_shop_item']
        # self.hash_tags = kwargs['hash_tags']
        self.hash_tags = []
        self.is_anonymous_shipping = kwargs['is_anonymous_shipping']
        self.is_web_visible = kwargs['is_web_visible']
        self.is_offerable = kwargs['is_offerable']
        self.is_organizational_user = kwargs['is_organizational_user']
        self.organizational_user_status = kwargs['organizational_user_status']
        self.is_stock_item = kwargs['is_stock_item']
        self.is_cancelable = kwargs['is_cancelable']
        self.shipped_by_worker = kwargs['shipped_by_worker']
        # self.additional_services = kwargs['additional_services']
        self.additional_services = []
        self.has_additional_service = kwargs['has_additional_service']
        self.has_like_list = kwargs['has_like_list']
        self.is_offerable_v2 = kwargs['is_offerable_v2']
        self.item_attributes = [ItemAttribute(**item) for item in kwargs['item_attributes']]  if 'item_attributes' in kwargs else []
        self.is_dismissed = kwargs['is_dismissed']
        self.photo_descriptions = kwargs['photo_descriptions'] if 'photo_descriptions' in kwargs else []
        self.meta_title = kwargs['meta_title']
        self.meta_subtitle = kwargs['meta_subtitle']
        # this is optional, only present if the item is an auction
        if "auction_info" in kwargs and kwargs["auction_info"] is not None:
            self.auction = ItemAuction(**kwargs['auction_info'])
        else:
            self.auction = None

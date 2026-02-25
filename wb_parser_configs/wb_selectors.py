from selenium.webdriver.common.by import By

class WBSerachSelectors:
    SEARCH_INPUT=(By.ID, "searchInput")

    PRODUCT_CARDS=(By.CLASS_NAME,"product-card-list")
    PRODUCT_CARD=(By.CLASS_NAME, "product-card__wrapper")
    PRODUCT_CARD_LINK=(By.CLASS_NAME,"product-card__link")

class WBSelectors:
    #TITLE=(By.CSS_SELECTOR, "[class*='productTitle']")
    TITLE=(By.TAG_NAME, "h3")

    ARTCLE=(By.XPATH, "//tr[contains(., 'Артикул')]//td")
    
    PRICE=(By.CSS_SELECTOR, "[class*='priceBlockFinalPric']")

    RATING=(By.CSS_SELECTOR, "[class*='user-opinion__rating-numb']")
    REVIEWS=(By.CSS_SELECTOR,"[class*='user-activity__count']")

    SELLER_INFO=(By.CSS_SELECTOR,"[class*='mainInfo']")
    SELLER_NAME=(By.CSS_SELECTOR,"[class*='name']")
    SELLER_LINK=(By.CSS_SELECTOR,"[class*='link']")

    SELLER_INFO_ALT=(By.CSS_SELECTOR,"[class*='sellerInfoDefaultChevron']")
    SELLER_NAME_ALT=(By.CSS_SELECTOR,"[class*='sellerInfoNameDefaultText']")
    SELLER_LINK_ALT=(By.CSS_SELECTOR,"[class*='sellerInfoButtonLink']")

    IMAGES_CONTAINER=(By.CSS_SELECTOR,"[class*='swiper']")
    IMAGES_ITEM=(By.CSS_SELECTOR,"[class*='swiper-slide'] img")

    EXPAND_INFO_BTN=(By.XPATH, "//*[contains(text(), 'Характеристики и описание')]")
    
    TABLE=(By.TAG_NAME, "table")
    ROW=(By.TAG_NAME,"tr")
    ROW_KEY=(By.TAG_NAME,'th')
    ROW_VAL=(By.TAG_NAME,'td')

    ABOUT=(By.CSS_SELECTOR, "[class*='descriptionText']")
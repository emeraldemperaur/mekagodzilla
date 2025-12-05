# HTTP RPA Test Entity Request Schemas
from pydantic import BaseModel, EmailStr, SecretStr
from typing import Optional, Literal
import datetime as dt

class GlobalGatewayCreateAccountTestEntityRPARequest(BaseModel):
    username: Optional[str] = None
    password: Optional[SecretStr] = None
    # Account Information
    account_name: str
    account_identifier: Optional[str] = None
    # Target Country
    entity_country: str
    # Test Entity Information
    entity_name: str
    entity_type: Optional[Literal['KYC', 'KYB', 'None']] = None
    # Name
    prefix: Optional[str] = None
    first_name: Optional[str] = None
    first_initial: Optional[str] = None
    middle_name: Optional[str] = None
    middle_inital: Optional[str] = None
    last_name: Optional[str] = None
    business_name: Optional[str] = None
    tradestyle_name: Optional[str] = None
    # Date of Birth
    date_of_birth: Optional[dt.date | str] = None
    date_of_birth_day: Optional[str] = None
    date_of_birth_month: Optional[str] = None
    date_of_birth_year: Optional[str] = None
    # Address
    address_1: Optional[str] = "123 Fake St"
    unit_number: Optional[int | str] = None
    building_number: Optional[str | int] = "123"
    civic_number: Optional[int | str] = None
    house_number: Optional[int | str] = None
    building_name: Optional[str] = None
    street_name: Optional[str] = "Fake"
    street_type: Optional[str] = "St"
    city: Optional[str] = "Fakesville"
    municipality: Optional[str] = None
    suburb: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    province: Optional[str] = "British Columbia"
    postal_code: Optional[str] = "A1B2C3"
    # Second Address
    second_unit_number: Optional[int | str] = None
    second_street_name: Optional[str] = None
    second_street_type: Optional[str] = None
    second_suburub: Optional[str] = None
    second_postal_code: Optional[str] = None
    second_state: Optional[str] = None
    second_street_number: Optional[str] = None
    # Business
    country: Optional[str] = None
    last_update_year: Optional[str] = None
    last_update_month: Optional[str] = None
    last_update_day: Optional[str] = None
    # Additional
    jurisdiction_of_incorporation: Optional[str] = None
    business_registration_number: Optional[str] = None
    cell_number: Optional[str] = "778-222-3232"
    telephone_2: Optional[str] = None
    email_address: Optional[EmailStr] = None
    duns_number: Optional[str] = None
    second_address_1: Optional[str] = None
    second_city: Optional[str] = None
    second_building_name: Optional[str] = None
    second_building_number: Optional[str] = None
    tax_id_number: Optional[str] = None
    enhanced_profile: Optional[str] = None
    filings: Optional[str] = None
    shareholder_list_document: Optional[str] = None
    year_of_incorporation: Optional[int] = None
    month_of_incorporation: Optional[int] = None
    day_of_incorporation: Optional[int] = None
    entities: Optional[str] = None
    people_of_significant_control: Optional[str] = None
    business_risk_values: Optional[str] = None
    social_insurance_number: Optional[str] = None
    social_security_number: Optional[str] = None
    second_county: Optional[str] = None
    ip_address: Optional[str] = None
    document_cost: Optional[str] = None
    document_meta_data: Optional[str] = None
    home_jurisdiction: Optional[str] = None
    watchlist_state: Optional[str] = None
    watchlist_data: Optional[str] = None
    watchlist_hit_details: Optional[str] = None
    address_association: Optional[str] = None
    phone_type: Optional[str] = "MOBILE"
    risk_level: Optional[str] = "Low"
    risk_description: Optional[str] = None
    mobile_sim_swap_date: Optional[str] = None
    field_used: Optional[str] = "Telephone"
    operator: Optional[str] = "Telus Mobility (supported)"
    watchlist_full_name: Optional[str] = None
    business_status: Optional[str] = None
    original_business_status: Optional[str] = None
    business_legal_form: Optional[str] = None
    original_business_legal_form: Optional[str] = None
    standardized_registration_number: Optional[str] = None
    standardized_locations: Optional[str] = None
    standardized_communication: Optional[str] = None
    standardized_share_capitals: Optional[str] = None
    standardized_industries: Optional[str] = None
    standardized_stock_exchanges: Optional[str] = None
    standardized_directors_officers: Optional[str] = None
    standardized_company_ownership_hierarchy: Optional[str] = None
    standardized_metadata: Optional[str] = None
    basic_product_called: Optional[str] = None
    basic_product_returned: Optional[str] = None
    enhanced_product_called: Optional[str] = None
    enhanced_product_returned: Optional[str] = None
    input_business_name_translated: Optional[str] = None
    input_business_name_transliterated: Optional[str] = None
    returned_business_name_translated: Optional[str] = None
    returned_business_name_transliterated: Optional[str] = None
    entities_product_called: Optional[str] = None
    entities_product_returned: Optional[str] = None
    warning: Optional[str] = None
    document_url: Optional[str] = None
    standardized_business_names: Optional[str] = None
    ownership_company_returned: Optional[str] = None
    standardized_incorporation_details: Optional[str] = None
    vendor_transactional_references: Optional[str] = None
    api_key_used: Optional[str] = None
    matching_scores: Optional[str] = None
    business_reference_id: Optional[str] = None
    name_details: Optional[str] = None
    address_details: Optional[str] = None
    phone_details: Optional[str] = None
    person_details: Optional[str] = None
    identification_details: Optional[str] = None
    result_information: Optional[str] = None
    comprehensive_view_metadata: Optional[str] = None
    phone_account_type: Optional[str] = None
    phone_account_user: Optional[str] = None
    phone_account_status: Optional[str] = None
    phone_contract_type: Optional[str] = None
    aml_assist_and_mobile_dual_process: Optional[str] = None
    aml_assist_credit_file_and_mobile_dual_process: Optional[str] = None
    canada_six_month_residency: Optional[str] = None
    fraud_flag: Optional[bool] = False
    three_year_credit: Optional[str] = None
    consumer_credit: Optional[str] = None
    fraud_message: Optional[str | int] = ("Consumer has been a victim of fraud and "
                                          "recommend failing to protect consumer.")
    is_deceased: Optional[bool] = False
    six_month_single_source: Optional[str] = None
    standardized_fillings: Optional[str] = None
    datasource_cost: Optional[str] = None
    respect_enhanced: Optional[bool] = False
    document_product_requested: Optional[str] = None
    document_product_returned: Optional[str] = None
    phone_risk_signals: Optional[str] = None
    email_risk_signals: Optional[str] = None
    ip_risk_signals: Optional[str] = None
    features_risk_signals: Optional[str] = None
    score_risk_signals: Optional[str] = None
    matching_details: Optional[str] = None
    telephone: Optional[str] = "123456789"
    gender: Optional[str] = None
    voter_id: Optional[str] = None
    national_id_type: Optional[str] = None
    national_id_number: Optional[str | int] = None
    province_code: Optional[str] = None
    state_province: Optional[str] = "BC"
    driver_licence_number: Optional[str] = None
    driver_licence_state: Optional[str] = None
    driver_licence_card_number: Optional[str] = None
    city_of_birth: Optional[str] = None
    state_of_birth: Optional[str] = None
    # Passport
    passport_number: Optional[str] = None
    country_of_birth: Optional[str] = None
    passport_country: Optional[str] = None
    notification: Optional[str] = None
    test_entity: Optional[dict[str, str | int | None]] = None
    # Australia
    medicare_reference: Optional[str] = None
    medicare_expiration_date: Optional[str] = None
    medicare_color: Optional[str] = None
    citizenship_acquisition_date: Optional[str] = None
    stock_number: Optional[str] = None
    au_immi_card_number: Optional[str | int] = None
    # Brazil
    national_id_status: Optional[str] = None
    year_of_death: Optional[str] = None
    # China/Taiwan
    given_name: Optional[str] = None
    surname: Optional[str] = None
    bank_account_number: Optional[str] = None
    # Hong Kong
    financial_information_document: Optional[str] = None
    annual_report: Optional[str] = None
    registration_details: Optional[str] = None
    # United Kingdom
    annual_accounts: Optional[str] = None
    article_of_association: Optional[str] = None
    capital_document: Optional[str] = None
    liquidation_document: Optional[str] = None
    mortgage_document: Optional[str] = None
    is_datasource_called: Optional[str] = None
    is_response_received: Optional[str] = None
    dual_process: Optional[str] = None
    # Ireland
    is_translation_supported: Optional[str] = None
    is_transliteration_supported: Optional[str] = None
    # New Zealand
    score: Optional[str] = None
    passport_expiration: Optional[str] = None
    driver_licence_version_number: Optional[str] = None
    vehicle_registration_plate: Optional[str] = None
    # Italy
    codice_fiscale: Optional[str] = None
    it_id_document_type: Optional[str] = None
    it_id_document_number: Optional[str] = None
    it_id_document_city_of_issue: Optional[str] = None
    it_id_document_province_of_issue: Optional[str] = None
    it_document_issue_date: Optional[str] = None

class GlobalGatewayCreateKYCSubAccountTestEntityRPARequest(BaseModel):
    username: Optional[str] = None
    password: Optional[SecretStr] = None
    # Account Information
    account_name: str
    subaccount_identifier: str
    account_identifier: Optional[str] = None
    # Target Country
    entity_country: str
    # Test Entity Information
    entity_name: str
    entity_type: Optional[Literal['KYC', 'KYB', 'None']] = None
    # Name
    prefix: Optional[str] = None
    first_name: str
    first_initial: Optional[str] = None
    middle_name: Optional[str] = None
    middle_inital: Optional[str] = None
    last_name: str
    # Date of Birth
    date_of_birth: Optional[dt.date | str] = None
    date_of_birth_day: Optional[str] = None
    date_of_birth_month: Optional[str] = None
    date_of_birth_year: Optional[str] = None
    # Address
    address_1: Optional[str] = "123 Fake St"
    unit_number: Optional[int | str] = None
    building_number: Optional[str | int] = "123"
    civic_number: Optional[int | str] = None
    house_number: Optional[int | str] = None
    building_name: Optional[str] = None
    street_name: Optional[str] = "Fake"
    street_type: Optional[str] = "St"
    city: Optional[str] = "Fakesville"
    municipality: Optional[str] = None
    suburb: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    province: Optional[str] = "British Columbia"
    postal_code: Optional[str] = "A1B2C3"
    # Driver's Licence
    driver_licence_number: Optional[str] = None
    driver_licence_state: Optional[str] = None
    driver_licence_card_number: Optional[str] = None
    # Passport
    passport_number: Optional[str] = None
    country_of_birth: Optional[str] = None
    passport_country: Optional[str] = None
    # Second Address
    second_unit_number: Optional[int | str] = None
    second_street_name: Optional[str] = None
    second_street_type: Optional[str] = None
    second_suburub: Optional[str] = None
    second_postal_code: Optional[str] = None
    second_state: Optional[str] = None
    second_street_number: Optional[str] = None
    # Business
    country: Optional[str] = None
    last_update_year: Optional[str] = None
    last_update_month: Optional[str] = None
    last_update_day: Optional[str] = None
    # Additional
    city_of_birth: Optional[str] = None
    state_of_birth: Optional[str] = None
    cell_number: Optional[str] = "778-222-3232"
    telephone_2: Optional[str] = None
    tax_id_number: Optional[str] = None
    email_address: Optional[EmailStr] = None
    authenticity_details: Optional[str] = None
    authenticity_reasons: Optional[str] = None
    social_insurance_number: Optional[str] = None
    social_security_number: Optional[str] = None
    address_association: Optional[str] = None
    phone_type: Optional[str] = "MOBILE"
    risk_level: Optional[str] = "Low"
    risk_description: Optional[str] = None
    mobile_sim_swap_date: Optional[str] = None
    field_used: Optional[str] = "Telephone"
    operator: Optional[str] = "Telus Mobility (supported)"
    phone_account_type: Optional[str] = None
    phone_account_user: Optional[str] = None
    phone_account_status: Optional[str] = None
    phone_contract_type: Optional[str] = None
    aml_assist_and_mobile_dual_process: Optional[str] = None
    aml_assist_credit_file_and_mobile_dual_process: Optional[str] = None
    canada_six_month_residency: Optional[str] = None
    fraud_flag: Optional[bool] = False
    three_year_credit: Optional[str] = None
    consumer_credit: Optional[str] = None
    fraud_message: Optional[str | int] = ("Consumer has been a victim of fraud and "
                                          "recommend failing to protect consumer.")
    matching_details: Optional[str] = None
    is_deceased: Optional[bool] = False
    six_month_single_source: Optional[str] = None
    telephone: Optional[str] = "123456789"
    national_id_number: Optional[str | int] = None
    gender: Optional[str] = None
    # Australia
    medicare_reference: Optional[str] = None
    medicare_expiration_date: Optional[str] = None
    medicare_color: Optional[str] = None
    citizenship_acquisition_date: Optional[str] = None
    stock_number: Optional[str] = None
    au_immi_card_number: Optional[str | int] = None
    # Brazil
    national_id_status: Optional[str] = None
    year_of_death: Optional[str] = None
    datasource_cost: Optional[str] = None
    # China/Taiwan
    bank_account_number: Optional[str] = None
    given_name: Optional[str] = None
    surname: Optional[str] = None
    # United Kingdom
    number_of_tradelines: Optional[str] = None
    tradeline_summary: Optional[str] = None
    dual_process: Optional[str] = None
    # Nigeria
    voter_id: Optional[str] = None
    national_id_type: Optional[str] = None
    # New Zealand
    score: Optional[str] = None
    passport_expiration: Optional[str] = None
    driver_licence_version_number: Optional[str] = None
    # Italy
    codice_fiscale: Optional[str] = None
    it_id_document_type: Optional[str] = None
    it_id_document_number: Optional[str] = None
    it_id_document_city_of_issue: Optional[str] = None
    it_id_document_province_of_issue: Optional[str] = None
    it_document_issue_date: Optional[str] = None
    # Japan
    city_town_village: Optional[str] = None
    subarea: Optional[str] = None
    prefecture: Optional[str] = None

    duns_number: Optional[str] = None
    second_address_1: Optional[str] = None
    second_city: Optional[str] = None
    second_building_name: Optional[str] = None
    second_building_number: Optional[str] = None
    enhanced_profile: Optional[str] = None
    filings: Optional[str] = None
    shareholder_list_document: Optional[str] = None
    year_of_incorporation: Optional[int] = None
    month_of_incorporation: Optional[int] = None
    day_of_incorporation: Optional[int] = None
    entities: Optional[str] = None
    people_of_significant_control: Optional[str] = None
    business_risk_values: Optional[str] = None

    second_county: Optional[str] = None
    ip_address: Optional[str] = None
    document_cost: Optional[str] = None
    document_meta_data: Optional[str] = None
    home_jurisdiction: Optional[str] = None
    watchlist_state: Optional[str] = None
    watchlist_data: Optional[str] = None
    watchlist_hit_details: Optional[str] = None
    watchlist_full_name: Optional[str] = None
    business_status: Optional[str] = None
    original_business_status: Optional[str] = None
    business_legal_form: Optional[str] = None
    original_business_legal_form: Optional[str] = None
    standardized_registration_number: Optional[str] = None
    standardized_locations: Optional[str] = None
    standardized_communication: Optional[str] = None
    standardized_share_capitals: Optional[str] = None
    standardized_industries: Optional[str] = None
    standardized_stock_exchanges: Optional[str] = None
    standardized_directors_officers: Optional[str] = None
    standardized_company_ownership_hierarchy: Optional[str] = None
    standardized_metadata: Optional[str] = None
    basic_product_called: Optional[str] = None
    basic_product_returned: Optional[str] = None
    enhanced_product_called: Optional[str] = None
    enhanced_product_returned: Optional[str] = None
    input_business_name_translated: Optional[str] = None
    input_business_name_transliterated: Optional[str] = None
    returned_business_name_translated: Optional[str] = None
    returned_business_name_transliterated: Optional[str] = None
    entities_product_called: Optional[str] = None
    entities_product_returned: Optional[str] = None
    warning: Optional[str] = None
    document_url: Optional[str] = None
    standardized_business_names: Optional[str] = None
    ownership_company_returned: Optional[str] = None
    standardized_incorporation_details: Optional[str] = None
    vendor_transactional_references: Optional[str] = None
    api_key_used: Optional[str] = None
    matching_scores: Optional[str] = None
    business_reference_id: Optional[str] = None
    name_details: Optional[str] = None
    address_details: Optional[str] = None
    phone_details: Optional[str] = None
    person_details: Optional[str] = None
    identification_details: Optional[str] = None
    result_information: Optional[str] = None
    comprehensive_view_metadata: Optional[str] = None


    standardized_fillings: Optional[str] = None
    respect_enhanced: Optional[bool] = False
    document_product_requested: Optional[str] = None
    document_product_returned: Optional[str] = None
    phone_risk_signals: Optional[str] = None
    email_risk_signals: Optional[str] = None
    ip_risk_signals: Optional[str] = None
    features_risk_signals: Optional[str] = None
    score_risk_signals: Optional[str] = None
    province_code: Optional[str] = None
    state_province: Optional[str] = "BC"


    notification: Optional[str] = None
    test_entity: Optional[dict[str, str | int | None]] = None



    # Hong Kong
    financial_information_document: Optional[str] = None
    annual_report: Optional[str] = None
    registration_details: Optional[str] = None
    # United Kingdom
    annual_accounts: Optional[str] = None
    article_of_association: Optional[str] = None
    capital_document: Optional[str] = None
    liquidation_document: Optional[str] = None
    mortgage_document: Optional[str] = None
    is_datasource_called: Optional[str] = None
    is_response_received: Optional[str] = None
    # Ireland
    is_translation_supported: Optional[str] = None
    is_transliteration_supported: Optional[str] = None


class GlobalGatewayCreateKYBSubAccountTestEntityRPARequest(BaseModel):
    username: Optional[str] = None
    password: Optional[SecretStr] = None
    # Account Information
    account_name: str
    subaccount_identifier: str
    account_identifier: Optional[str] = None
    # Target Country
    entity_country: str
    # Test Entity Information
    entity_name: str
    entity_type: Optional[Literal['KYC', 'KYB', 'None']] = None
    # Name
    prefix: Optional[str] = None
    first_name: Optional[str] = None
    first_initial: Optional[str] = None
    middle_name: Optional[str] = None
    middle_inital: Optional[str] = None
    last_name: Optional[str] = None
    business_name: str
    tradestyle_name: Optional[str] = None
    # Date of Birth
    date_of_birth: Optional[dt.date | str] = None
    date_of_birth_day: Optional[str] = None
    date_of_birth_month: Optional[str] = None
    date_of_birth_year: Optional[str] = None
    # Address
    address_1: Optional[str] = "123 Fake St"
    unit_number: Optional[int | str] = None
    building_number: Optional[str | int] = "123"
    civic_number: Optional[int | str] = None
    house_number: Optional[int | str] = None
    building_name: Optional[str] = None
    street_name: Optional[str] = "Fake"
    street_type: Optional[str] = "St"
    city: Optional[str] = "Fakesville"
    municipality: Optional[str] = None
    suburb: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    province: Optional[str] = "British Columbia"
    postal_code: Optional[str] = "A1B2C3"
    # Second Address
    second_unit_number: Optional[int | str] = None
    second_street_name: Optional[str] = None
    second_street_type: Optional[str] = None
    second_suburub: Optional[str] = None
    second_postal_code: Optional[str] = None
    second_state: Optional[str] = None
    second_street_number: Optional[str] = None
    # Business
    country: Optional[str] = None
    last_update_year: Optional[str] = None
    last_update_month: Optional[str] = None
    last_update_day: Optional[str] = None
    # Additional
    jurisdiction_of_incorporation: Optional[str] = None
    business_registration_number: Optional[str] = None
    cell_number: Optional[str] = "778-222-3232"
    telephone_2: Optional[str] = None
    email_address: Optional[EmailStr] = None
    duns_number: Optional[str] = None
    second_address_1: Optional[str] = None
    second_city: Optional[str] = None
    second_building_name: Optional[str] = None
    second_building_number: Optional[str] = None
    tax_id_number: Optional[str] = None
    enhanced_profile: Optional[str] = None
    filings: Optional[str] = None
    shareholder_list_document: Optional[str] = None
    year_of_incorporation: Optional[int] = None
    month_of_incorporation: Optional[int] = None
    day_of_incorporation: Optional[int] = None
    entities: Optional[str] = None
    people_of_significant_control: Optional[str] = None
    business_risk_values: Optional[str] = None
    social_insurance_number: Optional[str] = None
    social_security_number: Optional[str] = None
    second_county: Optional[str] = None
    ip_address: Optional[str] = None
    document_cost: Optional[str] = None
    document_meta_data: Optional[str] = None
    home_jurisdiction: Optional[str] = None
    watchlist_state: Optional[str] = None
    watchlist_data: Optional[str] = None
    watchlist_hit_details: Optional[str] = None
    phone_type: Optional[str] = "MOBILE"
    risk_level: Optional[str] = "Low"
    risk_description: Optional[str] = None
    mobile_sim_swap_date: Optional[str] = None
    field_used: Optional[str] = "Telephone"
    operator: Optional[str] = "Telus Mobility (supported)"
    watchlist_full_name: Optional[str] = None
    business_status: Optional[str] = None
    original_business_status: Optional[str] = None
    business_legal_form: Optional[str] = None
    original_business_legal_form: Optional[str] = None
    standardized_registration_number: Optional[str] = None
    standardized_locations: Optional[str] = None
    standardized_communication: Optional[str] = None
    standardized_share_capitals: Optional[str] = None
    standardized_industries: Optional[str] = None
    standardized_stock_exchanges: Optional[str] = None
    standardized_directors_officers: Optional[str] = None
    standardized_company_ownership_hierarchy: Optional[str] = None
    standardized_metadata: Optional[str] = None
    basic_product_called: Optional[str] = None
    basic_product_returned: Optional[str] = None
    enhanced_product_called: Optional[str] = None
    enhanced_product_returned: Optional[str] = None
    input_business_name_translated: Optional[str] = None
    input_business_name_transliterated: Optional[str] = None
    returned_business_name_translated: Optional[str] = None
    returned_business_name_transliterated: Optional[str] = None
    entities_product_called: Optional[str] = None
    entities_product_returned: Optional[str] = None
    warning: Optional[str] = None
    document_url: Optional[str] = None
    standardized_business_names: Optional[str] = None
    ownership_company_returned: Optional[str] = None
    standardized_incorporation_details: Optional[str] = None
    vendor_transactional_references: Optional[str] = None
    api_key_used: Optional[str] = None
    matching_scores: Optional[str] = None
    business_reference_id: Optional[str] = None
    name_details: Optional[str] = None
    address_details: Optional[str] = None
    phone_details: Optional[str] = None
    person_details: Optional[str] = None
    identification_details: Optional[str] = None
    result_information: Optional[str] = None
    comprehensive_view_metadata: Optional[str] = None
    phone_account_type: Optional[str] = None
    phone_account_user: Optional[str] = None
    phone_account_status: Optional[str] = None
    phone_contract_type: Optional[str] = None
    aml_assist_and_mobile_dual_process: Optional[str] = None
    aml_assist_credit_file_and_mobile_dual_process: Optional[str] = None
    canada_six_month_residency: Optional[str] = None
    fraud_flag: Optional[bool] = False
    three_year_credit: Optional[str] = None
    consumer_credit: Optional[str] = None
    fraud_message: Optional[str | int] = ("Consumer has been a victim of fraud and "
                                          "recommend failing to protect consumer.")
    is_deceased: Optional[bool] = False
    six_month_single_source: Optional[str] = None
    standardized_fillings: Optional[str] = None
    datasource_cost: Optional[str] = None
    respect_enhanced: Optional[bool] = False
    document_product_requested: Optional[str] = None
    document_product_returned: Optional[str] = None
    phone_risk_signals: Optional[str] = None
    email_risk_signals: Optional[str] = None
    ip_risk_signals: Optional[str] = None
    features_risk_signals: Optional[str] = None
    score_risk_signals: Optional[str] = None
    matching_details: Optional[str] = None
    telephone: Optional[str] = "123456789"
    gender: Optional[str] = None
    voter_id: Optional[str] = None
    national_id_type: Optional[str] = None
    national_id_number: Optional[str | int] = None
    province_code: Optional[str] = None
    state_province: Optional[str] = "BC"
    driver_licence_number: Optional[str] = None
    driver_licence_state: Optional[str] = None
    driver_licence_card_number: Optional[str] = None
    city_of_birth: Optional[str] = None
    state_of_birth: Optional[str] = None
    # Passport
    passport_number: Optional[str] = None
    country_of_birth: Optional[str] = None
    passport_country: Optional[str] = None
    notification: Optional[str] = None
    test_entity: Optional[dict[str, str | int | None]] = None

    # Brazil
    year_of_death: Optional[str] = None
    # China/Taiwan
    given_name: Optional[str] = None
    surname: Optional[str] = None
    # Hong Kong
    financial_information_document: Optional[str] = None
    annual_report: Optional[str] = None
    registration_details: Optional[str] = None
    # United Kingdom
    annual_accounts: Optional[str] = None
    article_of_association: Optional[str] = None
    capital_document: Optional[str] = None
    liquidation_document: Optional[str] = None
    mortgage_document: Optional[str] = None
    is_datasource_called: Optional[str] = None
    is_response_received: Optional[str] = None
    dual_process: Optional[str] = None
    # Ireland
    is_translation_supported: Optional[str] = None
    is_transliteration_supported: Optional[str] = None


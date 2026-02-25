from rest_framework import serializers


def validate_offer_details_count(details: list) -> list:
    if len(details) != 3:
        raise serializers.ValidationError('Ein Angebot muss genau 3 Details enthalten.')
    return details


def validate_offer_type_for_update(offer_type: str, allowed_types: set) -> None:
    if not offer_type or offer_type not in allowed_types:
        raise serializers.ValidationError(
            {'details': 'offer_type muss mitgegeben werden (basic/standard/premium).'}
        )
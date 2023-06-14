// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'limitation_factors.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

LimitationFactor _$LimitationFactorFromJson(Map<String, dynamic> json) =>
    LimitationFactor(
      id: json['id'] as int,
      name: json['name'] as String,
    );

Map<String, dynamic> _$LimitationFactorToJson(LimitationFactor instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
    };

LimitationFactors _$LimitationFactorsFromJson(Map<String, dynamic> json) =>
    LimitationFactors(
      values: (json['values'] as List<dynamic>)
          .map((e) => LimitationFactor.fromJson(e as Map<String, dynamic>))
          .toList(),
    );

Map<String, dynamic> _$LimitationFactorsToJson(LimitationFactors instance) =>
    <String, dynamic>{
      'values': instance.values,
    };

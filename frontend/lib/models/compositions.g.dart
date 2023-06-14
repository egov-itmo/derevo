// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'compositions.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Compositions _$CompositionsFromJson(Map<String, dynamic> json) => Compositions(
      compositions: (json['compositions'] as List<dynamic>)
          .map((e) => Plants.fromJson(e as Map<String, dynamic>))
          .toList(),
    );

Map<String, dynamic> _$CompositionsToJson(Compositions instance) =>
    <String, dynamic>{
      'compositions': instance.compositions,
    };

// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'plants.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Plant _$PlantFromJson(Map<String, dynamic> json) => Plant(
      id: json['id'] as int,
      nameRu: json['name_ru'] as String,
      nameLatin: json['name_latin'] as String,
      type: json['type'] as String,
      heightAvg: (json['height_avg'] as num?)?.toDouble(),
      crownDiameter: (json['crown_diameter'] as num?)?.toDouble(),
      spreadAggressivenessLevel: json['spread_aggressiveness_level'] as int?,
      survivabilityLevel: json['survivability_level'] as int?,
      isInvasive: json['is_invasive'] as bool?,
      genus: json['genus'] as String?,
      photoUrl: json['photo_url'] as String?,
    );

Map<String, dynamic> _$PlantToJson(Plant instance) => <String, dynamic>{
      'id': instance.id,
      'name_ru': instance.nameRu,
      'name_latin': instance.nameLatin,
      'type': instance.type,
      'height_avg': instance.heightAvg,
      'crown_diameter': instance.crownDiameter,
      'spread_aggressiveness_level': instance.spreadAggressivenessLevel,
      'survivability_level': instance.survivabilityLevel,
      'is_invasive': instance.isInvasive,
      'genus': instance.genus,
      'photo_url': instance.photoUrl,
    };

Plants _$PlantsFromJson(Map<String, dynamic> json) => Plants(
      plants: (json['plants'] as List<dynamic>)
          .map((e) => Plant.fromJson(e as Map<String, dynamic>))
          .toList(),
    );

Map<String, dynamic> _$PlantsToJson(Plants instance) => <String, dynamic>{
      'plants': instance.plants,
    };

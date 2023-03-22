import 'package:json_annotation/json_annotation.dart';

part 'limitation_factors.g.dart';

enum LimitationFactorType {
  humidityType,
  lightType,
  soilAcidityType,
  soilFertilityType,
  soilType
}

Map<LimitationFactorType, String> limitationFactorEndpoints = {
  LimitationFactorType.humidityType: "/api/listing/humidity_types",
  LimitationFactorType.lightType: "/api/listing/light_types",
  LimitationFactorType.soilAcidityType: "/api/listing/soil_acidity_types",
  LimitationFactorType.soilFertilityType: "/api/listing/soil_fertility_types",
  LimitationFactorType.soilType: "/api/listing/soil_types",
};

@JsonSerializable()
class LimitationFactor {
  final int id;
  final String name;

  LimitationFactor({required this.id, required this.name});

  factory LimitationFactor.fromJson(Map<String, dynamic> json) =>
      _$LimitationFactorFromJson(json);

  Map<String, dynamic> toJson() => _$LimitationFactorToJson(this);
}

@JsonSerializable()
class LimitationFactors {
  final List<LimitationFactor> values;

  LimitationFactors({required this.values});

  factory LimitationFactors.fromJson(Map<String, dynamic> json) =>
      _$LimitationFactorsFromJson(json);

  Map<String, dynamic> toJson() => _$LimitationFactorsToJson(this);
}

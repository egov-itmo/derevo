class AppConfig {
  String apiHost;

  AppConfig({required this.apiHost});
}

AppConfig appConfig = AppConfig(apiHost: "http://localhost:8080");

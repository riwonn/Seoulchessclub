import 'package:json_annotation/json_annotation.dart';
import 'user.dart';

part 'auth.g.dart';

// SMS 인증 요청
@JsonSerializable()
class SMSRequest {
  @JsonKey(name: 'phone_number')
  final String phoneNumber;

  SMSRequest({required this.phoneNumber});

  factory SMSRequest.fromJson(Map<String, dynamic> json) =>
      _$SMSRequestFromJson(json);
  Map<String, dynamic> toJson() => _$SMSRequestToJson(this);
}

// SMS 인증 확인
@JsonSerializable()
class SMSVerify {
  @JsonKey(name: 'phone_number')
  final String phoneNumber;
  final String code;

  SMSVerify({
    required this.phoneNumber,
    required this.code,
  });

  factory SMSVerify.fromJson(Map<String, dynamic> json) =>
      _$SMSVerifyFromJson(json);
  Map<String, dynamic> toJson() => _$SMSVerifyToJson(this);
}

// 로그인 요청
@JsonSerializable()
class LoginRequest {
  @JsonKey(name: 'phone_number')
  final String phoneNumber;

  LoginRequest({required this.phoneNumber});

  factory LoginRequest.fromJson(Map<String, dynamic> json) =>
      _$LoginRequestFromJson(json);
  Map<String, dynamic> toJson() => _$LoginRequestToJson(this);
}

// 로그인 응답
@JsonSerializable()
class LoginResponse {
  @JsonKey(name: 'access_token')
  final String accessToken;
  @JsonKey(name: 'token_type')
  final String tokenType;
  final User user;

  LoginResponse({
    required this.accessToken,
    required this.tokenType,
    required this.user,
  });

  factory LoginResponse.fromJson(Map<String, dynamic> json) =>
      _$LoginResponseFromJson(json);
  Map<String, dynamic> toJson() => _$LoginResponseToJson(this);
}


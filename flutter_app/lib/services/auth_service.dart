import 'package:dio/dio.dart';
import '../models/auth.dart';
import '../models/user.dart';
import 'api_service.dart';

class AuthService {
  final ApiService _apiService;

  AuthService({required ApiService apiService}) : _apiService = apiService;
  
  // SocialAuthService에서 접근하기 위한 getter
  ApiService get apiService => _apiService;

  /// SMS 인증 코드 요청
  Future<void> requestSMS(String phoneNumber) async {
    try {
      final response = await _apiService.post(
        '/sms/request',
        data: SMSRequest(phoneNumber: phoneNumber).toJson(),
      );

      if (response.statusCode != 200) {
        throw Exception('SMS 전송 실패');
      }
    } on DioException catch (e) {
      if (e.response?.statusCode == 429) {
        throw Exception('너무 많은 요청입니다. 잠시 후 다시 시도해주세요.');
      }
      throw Exception('SMS 전송 중 오류가 발생했습니다: ${e.message}');
    }
  }

  /// SMS 인증 코드 확인
  Future<void> verifySMS(String phoneNumber, String code) async {
    try {
      final response = await _apiService.post(
        '/sms/verify',
        data: SMSVerify(phoneNumber: phoneNumber, code: code).toJson(),
      );

      if (response.statusCode != 200) {
        throw Exception('인증 실패');
      }
    } on DioException catch (e) {
      if (e.response?.statusCode == 400) {
        final detail = e.response?.data['detail'];
        if (detail?.contains('expired') == true) {
          throw Exception('인증 코드가 만료되었습니다.');
        } else if (detail?.contains('invalid') == true) {
          throw Exception('잘못된 인증 코드입니다.');
        }
      }
      throw Exception('인증 중 오류가 발생했습니다: ${e.message}');
    }
  }

  /// 회원가입
  Future<User> register(UserCreate userData) async {
    try {
      final response = await _apiService.post(
        '/register',
        data: userData.toJson(),
      );

      if (response.statusCode == 201 || response.statusCode == 200) {
        return User.fromJson(response.data);
      } else {
        throw Exception('회원가입 실패');
      }
    } on DioException catch (e) {
      if (e.response?.statusCode == 403) {
        throw Exception('등록이 마감되었습니다. 정원이 초과되었습니다.');
      } else if (e.response?.statusCode == 409) {
        throw Exception('이미 등록된 전화번호 또는 이메일입니다.');
      }
      throw Exception('회원가입 중 오류가 발생했습니다: ${e.message}');
    }
  }

  /// 로그인 (JWT 토큰 발급)
  Future<LoginResponse> login(String phoneNumber) async {
    try {
      final response = await _apiService.post(
        '/auth/login',
        data: LoginRequest(phoneNumber: phoneNumber).toJson(),
      );

      if (response.statusCode == 200) {
        final loginResponse = LoginResponse.fromJson(response.data);
        
        // 토큰 저장
        await _apiService.saveToken(loginResponse.accessToken);
        
        return loginResponse;
      } else {
        throw Exception('로그인 실패');
      }
    } on DioException catch (e) {
      if (e.response?.statusCode == 404) {
        throw Exception('등록되지 않은 사용자입니다. 회원가입을 먼저 진행해주세요.');
      }
      throw Exception('로그인 중 오류가 발생했습니다: ${e.message}');
    }
  }

  /// 현재 로그인한 사용자 정보 조회
  Future<User> getCurrentUser() async {
    try {
      final response = await _apiService.get('/auth/me');

      if (response.statusCode == 200) {
        return User.fromJson(response.data);
      } else {
        throw Exception('사용자 정보 조회 실패');
      }
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        throw Exception('인증이 만료되었습니다. 다시 로그인해주세요.');
      }
      throw Exception('사용자 정보 조회 중 오류가 발생했습니다: ${e.message}');
    }
  }

  /// 로그아웃
  Future<void> logout() async {
    await _apiService.clearToken();
  }

  /// 전화번호로 사용자 조회 (재방문 고객 인식)
  Future<User?> getUserByPhone(String phoneNumber) async {
    try {
      final response = await _apiService.get(
        '/get_user_by_phone',
        queryParameters: {'phone_number': phoneNumber},
      );

      if (response.statusCode == 200) {
        return User.fromJson(response.data);
      }
      return null;
    } on DioException catch (e) {
      if (e.response?.statusCode == 404) {
        return null; // 사용자 없음
      }
      throw Exception('사용자 조회 중 오류가 발생했습니다: ${e.message}');
    }
  }

  /// 토큰 존재 여부 확인
  Future<bool> hasToken() async {
    final token = await _apiService.getToken();
    return token != null && token.isNotEmpty;
  }
}


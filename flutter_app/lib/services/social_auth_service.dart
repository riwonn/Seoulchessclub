import 'package:sign_in_with_apple/sign_in_with_apple.dart';
import 'package:kakao_flutter_sdk_user/kakao_flutter_sdk_user.dart';
import 'package:dio/dio.dart';
import 'api_service.dart';
import '../models/user.dart';

class SocialAuthService {
  final ApiService _apiService;

  SocialAuthService({required ApiService apiService})
      : _apiService = apiService;

  /// Apple 로그인
  Future<SocialLoginResult> signInWithApple() async {
    try {
      // 1. Apple Sign In 요청
      final credential = await SignInWithApple.getAppleIDCredential(
        scopes: [
          AppleIDAuthorizationScopes.email,
          AppleIDAuthorizationScopes.fullName,
        ],
      );

      // 2. 백엔드 API로 토큰 전송
      final response = await _apiService.post(
        '/auth/apple',
        data: {
          'identity_token': credential.identityToken,
          'authorization_code': credential.authorizationCode,
          'user_info': credential.givenName != null || credential.familyName != null
              ? {
                  'name': {
                    'firstName': credential.givenName,
                    'lastName': credential.familyName,
                  }
                }
              : null,
        },
      );

      if (response.statusCode == 200) {
        final data = response.data;
        final user = User.fromJson(data['user']);
        final accessToken = data['access_token'] as String;
        final isNewUser = data['is_new_user'] as bool;

        // 토큰 저장
        await _apiService.saveToken(accessToken);

        return SocialLoginResult(
          user: user,
          accessToken: accessToken,
          isNewUser: isNewUser,
        );
      } else {
        throw Exception('Apple login failed');
      }
    } on SignInWithAppleAuthorizationException catch (e) {
      if (e.code == AuthorizationErrorCode.canceled) {
        throw Exception('Apple 로그인이 취소되었습니다');
      } else if (e.code == AuthorizationErrorCode.failed) {
        throw Exception('Apple 로그인에 실패했습니다');
      } else {
        throw Exception('Apple 로그인 중 오류가 발생했습니다: ${e.message}');
      }
    } on DioException catch (e) {
      throw Exception('Apple 로그인 API 오류: ${e.message}');
    } catch (e) {
      throw Exception('Apple 로그인 중 알 수 없는 오류가 발생했습니다: $e');
    }
  }

  /// 카카오 로그인
  Future<SocialLoginResult> signInWithKakao() async {
    try {
      // 1. 카카오톡 설치 여부 확인
      bool isKakaoTalkInstalled = await isKakaoTalkInstalled();

      OAuthToken token;
      if (isKakaoTalkInstalled) {
        // 카카오톡으로 로그인
        token = await UserApi.instance.loginWithKakaoTalk();
      } else {
        // 카카오 계정으로 로그인
        token = await UserApi.instance.loginWithKakaoAccount();
      }

      // 2. 백엔드 API로 액세스 토큰 전송
      final response = await _apiService.post(
        '/auth/kakao',
        data: {
          'access_token': token.accessToken,
        },
      );

      if (response.statusCode == 200) {
        final data = response.data;
        final user = User.fromJson(data['user']);
        final accessToken = data['access_token'] as String;
        final isNewUser = data['is_new_user'] as bool;

        // 토큰 저장
        await _apiService.saveToken(accessToken);

        return SocialLoginResult(
          user: user,
          accessToken: accessToken,
          isNewUser: isNewUser,
        );
      } else {
        throw Exception('Kakao login failed');
      }
    } catch (e) {
      if (e.toString().contains('사용자가 취소')) {
        throw Exception('카카오 로그인이 취소되었습니다');
      }
      throw Exception('카카오 로그인 중 오류가 발생했습니다: $e');
    }
  }

  /// Apple 로그인 가능 여부 확인
  Future<bool> isAppleSignInAvailable() async {
    try {
      return await SignInWithApple.isAvailable();
    } catch (e) {
      return false;
    }
  }
}

/// 소셜 로그인 결과
class SocialLoginResult {
  final User user;
  final String accessToken;
  final bool isNewUser;

  SocialLoginResult({
    required this.user,
    required this.accessToken,
    required this.isNewUser,
  });
}


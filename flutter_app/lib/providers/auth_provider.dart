import 'package:flutter/foundation.dart';
import '../models/user.dart';
import '../services/auth_service.dart';
import '../services/social_auth_service.dart';

class AuthProvider with ChangeNotifier {
  final AuthService _authService;
  late final SocialAuthService _socialAuthService;
  
  User? _currentUser;
  bool _isAuthenticated = false;
  bool _isLoading = true;

  AuthProvider({required AuthService authService}) 
      : _authService = authService {
    _socialAuthService = SocialAuthService(apiService: authService.apiService);
    _initAuth();
  }

  User? get currentUser => _currentUser;
  bool get isAuthenticated => _isAuthenticated;
  bool get isLoading => _isLoading;

  /// 앱 시작 시 인증 상태 초기화
  Future<void> _initAuth() async {
    try {
      final hasToken = await _authService.hasToken();
      
      if (hasToken) {
        // 토큰이 있으면 사용자 정보 가져오기
        _currentUser = await _authService.getCurrentUser();
        _isAuthenticated = true;
      }
    } catch (e) {
      // 토큰이 유효하지 않으면 로그아웃 처리
      await logout();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// SMS 인증 코드 요청
  Future<void> requestSMS(String phoneNumber) async {
    try {
      await _authService.requestSMS(phoneNumber);
    } catch (e) {
      rethrow;
    }
  }

  /// SMS 인증 코드 확인
  Future<void> verifySMS(String phoneNumber, String code) async {
    try {
      await _authService.verifySMS(phoneNumber, code);
    } catch (e) {
      rethrow;
    }
  }

  /// 회원가입
  Future<User> register(UserCreate userData) async {
    try {
      final user = await _authService.register(userData);
      return user;
    } catch (e) {
      rethrow;
    }
  }

  /// 로그인
  Future<void> login(String phoneNumber) async {
    try {
      final loginResponse = await _authService.login(phoneNumber);
      _currentUser = loginResponse.user;
      _isAuthenticated = true;
      notifyListeners();
    } catch (e) {
      rethrow;
    }
  }

  /// 로그아웃
  Future<void> logout() async {
    await _authService.logout();
    _currentUser = null;
    _isAuthenticated = false;
    notifyListeners();
  }

  /// 사용자 정보 새로고침
  Future<void> refreshUser() async {
    try {
      if (_isAuthenticated) {
        _currentUser = await _authService.getCurrentUser();
        notifyListeners();
      }
    } catch (e) {
      // 토큰이 만료되었으면 로그아웃
      await logout();
    }
  }

  /// 전화번호로 사용자 조회 (재방문 고객 인식)
  Future<User?> getUserByPhone(String phoneNumber) async {
    try {
      return await _authService.getUserByPhone(phoneNumber);
    } catch (e) {
      rethrow;
    }
  }

  /// Apple 로그인
  Future<void> signInWithApple() async {
    try {
      final result = await _socialAuthService.signInWithApple();
      _currentUser = result.user;
      _isAuthenticated = true;
      notifyListeners();
    } catch (e) {
      rethrow;
    }
  }

  /// 카카오 로그인
  Future<void> signInWithKakao() async {
    try {
      final result = await _socialAuthService.signInWithKakao();
      _currentUser = result.user;
      _isAuthenticated = true;
      notifyListeners();
    } catch (e) {
      rethrow;
    }
  }

  /// Apple 로그인 가능 여부 확인
  Future<bool> isAppleSignInAvailable() async {
    return await _socialAuthService.isAppleSignInAvailable();
  }
}


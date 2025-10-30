import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import 'package:kakao_flutter_sdk_user/kakao_flutter_sdk_user.dart';

import 'services/api_service.dart';
import 'services/auth_service.dart';
import 'providers/auth_provider.dart';
import 'providers/meeting_provider.dart';
import 'screens/splash_screen.dart';
import 'screens/auth/phone_verification_screen.dart';
import 'screens/auth/registration_screen.dart';
import 'screens/home/home_screen.dart';
import 'screens/meetings/meetings_list_screen.dart';
import 'screens/profile/profile_screen.dart';

void main() {
  // 카카오 SDK 초기화
  KakaoSdk.init(
    nativeAppKey: 'YOUR_KAKAO_NATIVE_APP_KEY', // 카카오 개발자 콘솔에서 발급받은 네이티브 앱 키
    javaScriptAppKey: 'YOUR_KAKAO_JAVASCRIPT_APP_KEY', // 카카오 개발자 콘솔에서 발급받은 JavaScript 앱 키
  );
  
  runApp(const CommunityControlApp());
}

class CommunityControlApp extends StatelessWidget {
  const CommunityControlApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        // 서비스 프로바이더
        Provider<ApiService>(
          create: (_) => ApiService(),
        ),
        Provider<AuthService>(
          create: (context) => AuthService(
            apiService: context.read<ApiService>(),
          ),
        ),
        
        // 상태 관리 프로바이더
        ChangeNotifierProvider<AuthProvider>(
          create: (context) => AuthProvider(
            authService: context.read<AuthService>(),
          ),
        ),
        ChangeNotifierProvider<MeetingProvider>(
          create: (context) => MeetingProvider(
            apiService: context.read<ApiService>(),
          ),
        ),
      ],
      child: Consumer<AuthProvider>(
        builder: (context, authProvider, _) {
          return MaterialApp.router(
            title: 'Community Control',
            theme: ThemeData(
              primarySwatch: Colors.blue,
              useMaterial3: true,
              appBarTheme: const AppBarTheme(
                centerTitle: true,
                elevation: 0,
              ),
              inputDecorationTheme: InputDecorationTheme(
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                filled: true,
                fillColor: Colors.grey[50],
              ),
              elevatedButtonTheme: ElevatedButtonThemeData(
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 32,
                    vertical: 16,
                  ),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
            ),
            routerConfig: _router(authProvider),
          );
        },
      ),
    );
  }

  // 라우터 설정
  GoRouter _router(AuthProvider authProvider) {
    return GoRouter(
      initialLocation: '/splash',
      redirect: (context, state) {
        final isLoggedIn = authProvider.isAuthenticated;
        final isOnAuthPage = state.matchedLocation.startsWith('/auth');
        final isOnSplash = state.matchedLocation == '/splash';

        // 스플래시 화면은 항상 허용
        if (isOnSplash) {
          return null;
        }

        // 로그인되지 않았고 인증 페이지가 아니면 인증 페이지로 리다이렉트
        if (!isLoggedIn && !isOnAuthPage) {
          return '/auth/phone';
        }

        // 로그인되었는데 인증 페이지에 있으면 홈으로 리다이렉트
        if (isLoggedIn && isOnAuthPage) {
          return '/home';
        }

        return null;
      },
      routes: [
        GoRoute(
          path: '/splash',
          builder: (context, state) => const SplashScreen(),
        ),
        GoRoute(
          path: '/auth/phone',
          builder: (context, state) => const PhoneVerificationScreen(),
        ),
        GoRoute(
          path: '/auth/register',
          builder: (context, state) {
            final phoneNumber = state.uri.queryParameters['phone'] ?? '';
            return RegistrationScreen(phoneNumber: phoneNumber);
          },
        ),
        GoRoute(
          path: '/home',
          builder: (context, state) => const HomeScreen(),
        ),
        GoRoute(
          path: '/meetings',
          builder: (context, state) => const MeetingsListScreen(),
        ),
        GoRoute(
          path: '/profile',
          builder: (context, state) => const ProfileScreen(),
        ),
      ],
    );
  }
}


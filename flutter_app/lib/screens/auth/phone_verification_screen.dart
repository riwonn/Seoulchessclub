import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import '../../providers/auth_provider.dart';

class PhoneVerificationScreen extends StatefulWidget {
  const PhoneVerificationScreen({super.key});

  @override
  State<PhoneVerificationScreen> createState() =>
      _PhoneVerificationScreenState();
}

class _PhoneVerificationScreenState extends State<PhoneVerificationScreen> {
  final _phoneController = TextEditingController();
  final _codeController = TextEditingController();
  bool _isCodeSent = false;
  bool _isLoading = false;
  String? _error;
  bool _isAppleSignInAvailable = false;

  @override
  void initState() {
    super.initState();
    _checkAppleSignInAvailability();
  }

  Future<void> _checkAppleSignInAvailability() async {
    final authProvider = context.read<AuthProvider>();
    final available = await authProvider.isAppleSignInAvailable();
    setState(() => _isAppleSignInAvailable = available);
  }

  @override
  void dispose() {
    _phoneController.dispose();
    _codeController.dispose();
    super.dispose();
  }

  Future<void> _sendSMS() async {
    if (_phoneController.text.isEmpty) {
      setState(() => _error = '전화번호를 입력해주세요');
      return;
    }

    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final authProvider = context.read<AuthProvider>();
      await authProvider.requestSMS(_phoneController.text);
      
      setState(() {
        _isCodeSent = true;
        _isLoading = false;
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('인증 코드가 전송되었습니다')),
        );
      }
    } catch (e) {
      setState(() {
        _error = e.toString().replaceAll('Exception: ', '');
        _isLoading = false;
      });
    }
  }

  Future<void> _verifyCode() async {
    if (_codeController.text.isEmpty) {
      setState(() => _error = '인증 코드를 입력해주세요');
      return;
    }

    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final authProvider = context.read<AuthProvider>();
      
      // 1. SMS 인증 확인
      await authProvider.verifySMS(_phoneController.text, _codeController.text);
      
      // 2. 기존 사용자인지 확인
      final existingUser = await authProvider.getUserByPhone(_phoneController.text);
      
      if (existingUser != null) {
        // 기존 사용자: 로그인
        await authProvider.login(_phoneController.text);
        
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('환영합니다, ${existingUser.name}님!')),
          );
          context.go('/home');
        }
      } else {
        // 신규 사용자: 회원가입 페이지로 이동
        if (mounted) {
          context.go('/auth/register?phone=${_phoneController.text}');
        }
      }
    } catch (e) {
      setState(() {
        _error = e.toString().replaceAll('Exception: ', '');
        _isLoading = false;
      });
    }
  }

  Future<void> _signInWithApple() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final authProvider = context.read<AuthProvider>();
      await authProvider.signInWithApple();
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Apple 로그인 성공!')),
        );
        context.go('/home');
      }
    } catch (e) {
      setState(() {
        _error = e.toString().replaceAll('Exception: ', '');
        _isLoading = false;
      });
    }
  }

  Future<void> _signInWithKakao() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final authProvider = context.read<AuthProvider>();
      await authProvider.signInWithKakao();
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('카카오 로그인 성공!')),
        );
        context.go('/home');
      }
    } catch (e) {
      setState(() {
        _error = e.toString().replaceAll('Exception: ', '');
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('전화번호 인증'),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 32),
              const Text(
                '전화번호로 로그인',
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              const Text(
                'SMS 인증을 통해 안전하게 로그인하세요',
                style: TextStyle(
                  fontSize: 16,
                  color: Colors.grey,
                ),
              ),
              const SizedBox(height: 48),
              
              // 전화번호 입력
              TextField(
                controller: _phoneController,
                keyboardType: TextInputType.phone,
                enabled: !_isCodeSent,
                decoration: InputDecoration(
                  labelText: '전화번호',
                  hintText: '01012345678',
                  prefixIcon: const Icon(Icons.phone),
                  suffixIcon: _isCodeSent
                      ? const Icon(Icons.check_circle, color: Colors.green)
                      : null,
                ),
              ),
              const SizedBox(height: 16),
              
              // SMS 전송 버튼
              if (!_isCodeSent)
                ElevatedButton(
                  onPressed: _isLoading ? null : _sendSMS,
                  child: _isLoading
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text('인증 코드 받기'),
                ),
              
              // 인증 코드 입력 (SMS 전송 후)
              if (_isCodeSent) ...[
                TextField(
                  controller: _codeController,
                  keyboardType: TextInputType.number,
                  maxLength: 6,
                  decoration: const InputDecoration(
                    labelText: '인증 코드',
                    hintText: '6자리 숫자',
                    prefixIcon: Icon(Icons.lock),
                  ),
                ),
                const SizedBox(height: 16),
                ElevatedButton(
                  onPressed: _isLoading ? null : _verifyCode,
                  child: _isLoading
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text('인증 확인'),
                ),
                const SizedBox(height: 16),
                TextButton(
                  onPressed: () {
                    setState(() {
                      _isCodeSent = false;
                      _codeController.clear();
                      _error = null;
                    });
                  },
                  child: const Text('다른 번호로 변경'),
                ),
              ],
              
              // 에러 메시지
              if (_error != null) ...[
                const SizedBox(height: 16),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.red.shade50,
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.red.shade200),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.error_outline, color: Colors.red.shade700),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          _error!,
                          style: TextStyle(color: Colors.red.shade700),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
              
              const Spacer(),
              
              // 구분선
              Row(
                children: [
                  const Expanded(child: Divider()),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16),
                    child: Text(
                      '또는',
                      style: TextStyle(
                        color: Colors.grey.shade600,
                        fontSize: 14,
                      ),
                    ),
                  ),
                  const Expanded(child: Divider()),
                ],
              ),
              const SizedBox(height: 24),
              
              // 소셜 로그인 버튼
              if (_isAppleSignInAvailable)
                _SocialLoginButton(
                  onPressed: _isLoading ? null : _signInWithApple,
                  icon: Icons.apple,
                  label: 'Apple로 로그인',
                  backgroundColor: Colors.black,
                  textColor: Colors.white,
                ),
              const SizedBox(height: 12),
              
              _SocialLoginButton(
                onPressed: _isLoading ? null : _signInWithKakao,
                icon: Icons.chat_bubble,
                label: '카카오로 로그인',
                backgroundColor: const Color(0xFFFEE500),
                textColor: Colors.black87,
              ),
              const SizedBox(height: 24),
              
              // 안내 문구
              const Text(
                '※ 신규 사용자는 인증 후 회원가입 페이지로 이동합니다',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.grey,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _SocialLoginButton extends StatelessWidget {
  final VoidCallback? onPressed;
  final IconData icon;
  final String label;
  final Color backgroundColor;
  final Color textColor;

  const _SocialLoginButton({
    required this.onPressed,
    required this.icon,
    required this.label,
    required this.backgroundColor,
    required this.textColor,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      child: ElevatedButton.icon(
        onPressed: onPressed,
        icon: Icon(icon, color: textColor),
        label: Text(label),
        style: ElevatedButton.styleFrom(
          backgroundColor: backgroundColor,
          foregroundColor: textColor,
          padding: const EdgeInsets.symmetric(vertical: 16),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
      ),
    );
  }
}


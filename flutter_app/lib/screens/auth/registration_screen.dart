import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import '../../models/user.dart';
import '../../providers/auth_provider.dart';

class RegistrationScreen extends StatefulWidget {
  final String phoneNumber;

  const RegistrationScreen({
    super.key,
    required this.phoneNumber,
  });

  @override
  State<RegistrationScreen> createState() => _RegistrationScreenState();
}

class _RegistrationScreenState extends State<RegistrationScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _birthYearController = TextEditingController();
  
  String _gender = 'MALE';
  String _chessExperience = 'NO_BUT_WANT_TO_LEARN';
  String? _chessRating;
  bool _isLoading = false;
  String? _error;

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _birthYearController.dispose();
    super.dispose();
  }

  Future<void> _register() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final authProvider = context.read<AuthProvider>();
      
      final userData = UserCreate(
        name: _nameController.text,
        phoneNumber: widget.phoneNumber,
        email: _emailController.text,
        gender: _gender,
        birthYear: _birthYearController.text.isNotEmpty
            ? int.tryParse(_birthYearController.text)
            : null,
        chessExperience: _chessExperience,
        chessRating: _chessRating,
      );

      // 회원가입
      await authProvider.register(userData);
      
      // 로그인
      await authProvider.login(widget.phoneNumber);

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('환영합니다! 회원가입이 완료되었습니다')),
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
        title: const Text('회원가입'),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Text(
                  '회원 정보 입력',
                  style: TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  '전화번호: ${widget.phoneNumber}',
                  style: const TextStyle(
                    fontSize: 16,
                    color: Colors.grey,
                  ),
                ),
                const SizedBox(height: 32),
                
                // 이름
                TextFormField(
                  controller: _nameController,
                  decoration: const InputDecoration(
                    labelText: '이름 *',
                    prefixIcon: Icon(Icons.person),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return '이름을 입력해주세요';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 16),
                
                // 이메일
                TextFormField(
                  controller: _emailController,
                  keyboardType: TextInputType.emailAddress,
                  decoration: const InputDecoration(
                    labelText: '이메일 *',
                    prefixIcon: Icon(Icons.email),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return '이메일을 입력해주세요';
                    }
                    if (!value.contains('@')) {
                      return '올바른 이메일 형식이 아닙니다';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 16),
                
                // 성별
                DropdownButtonFormField<String>(
                  value: _gender,
                  decoration: const InputDecoration(
                    labelText: '성별 *',
                    prefixIcon: Icon(Icons.people),
                  ),
                  items: const [
                    DropdownMenuItem(value: 'MALE', child: Text('남성')),
                    DropdownMenuItem(value: 'FEMALE', child: Text('여성')),
                    DropdownMenuItem(value: 'OTHER', child: Text('기타')),
                  ],
                  onChanged: (value) {
                    if (value != null) {
                      setState(() => _gender = value);
                    }
                  },
                ),
                const SizedBox(height: 16),
                
                // 출생년도
                TextFormField(
                  controller: _birthYearController,
                  keyboardType: TextInputType.number,
                  decoration: const InputDecoration(
                    labelText: '출생년도 (선택)',
                    hintText: '예: 1990',
                    prefixIcon: Icon(Icons.cake),
                  ),
                  validator: (value) {
                    if (value != null && value.isNotEmpty) {
                      final year = int.tryParse(value);
                      if (year == null || year < 1900 || year > 2024) {
                        return '올바른 출생년도를 입력해주세요';
                      }
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 16),
                
                // 체스 경험
                DropdownButtonFormField<String>(
                  value: _chessExperience,
                  decoration: const InputDecoration(
                    labelText: '체스 경험 *',
                    prefixIcon: Icon(Icons.extension),
                  ),
                  items: const [
                    DropdownMenuItem(
                      value: 'NO_BUT_WANT_TO_LEARN',
                      child: Text('아니요, 배우고 싶어요'),
                    ),
                    DropdownMenuItem(
                      value: 'KNOW_RULES_ONLY',
                      child: Text('규칙만 알아요'),
                    ),
                    DropdownMenuItem(
                      value: 'OCCASIONALLY_PLAY',
                      child: Text('가끔 둡니다'),
                    ),
                    DropdownMenuItem(
                      value: 'PLAY_WELL',
                      child: Text('잘 둡니다'),
                    ),
                  ],
                  onChanged: (value) {
                    if (value != null) {
                      setState(() => _chessExperience = value);
                    }
                  },
                ),
                const SizedBox(height: 16),
                
                // 체스 레이팅
                DropdownButtonFormField<String>(
                  value: _chessRating,
                  decoration: const InputDecoration(
                    labelText: '체스 레이팅 (선택)',
                    prefixIcon: Icon(Icons.star),
                  ),
                  items: const [
                    DropdownMenuItem(value: null, child: Text('선택 안 함')),
                    DropdownMenuItem(
                      value: 'I_DONT_KNOW',
                      child: Text('모르겠어요'),
                    ),
                    DropdownMenuItem(
                      value: 'UNDER_1000',
                      child: Text('1000 이하'),
                    ),
                    DropdownMenuItem(
                      value: 'BETWEEN_1000_1500',
                      child: Text('1000-1500'),
                    ),
                    DropdownMenuItem(
                      value: 'BETWEEN_1500_2000',
                      child: Text('1500-2000'),
                    ),
                    DropdownMenuItem(
                      value: 'OVER_2000',
                      child: Text('2000 이상'),
                    ),
                  ],
                  onChanged: (value) {
                    setState(() => _chessRating = value);
                  },
                ),
                const SizedBox(height: 32),
                
                // 에러 메시지
                if (_error != null) ...[
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
                  const SizedBox(height: 16),
                ],
                
                // 가입 버튼
                ElevatedButton(
                  onPressed: _isLoading ? null : _register,
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                  child: _isLoading
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text('가입 완료'),
                ),
                const SizedBox(height: 16),
                
                const Text(
                  '* 필수 입력 항목',
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
      ),
    );
  }
}


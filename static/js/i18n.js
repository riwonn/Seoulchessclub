// 다국어 지원 시스템
const translations = {
    ko: {
        // 공통
        back: "뒤로",
        confirm: "확인",
        cancel: "취소",
        loading: "처리 중...",
        error: "오류",
        success: "성공",
        
        // 모임 리스트
        upcomingMeetings: "다가오는 모임",
        subtitle: "체스, 커피, 그리고 좋은 대화를 함께해요",
        welcomeUser: "님, 오늘은 어떤 모임을 신청할까요?",
        registerPrompt: "회원가입하고 모임에 참가하세요!",
        registerButton: "회원가입하기",
        capacity: "정원",
        people: "명",
        registerMeeting: "참가 신청",
        noMeetings: "예정된 모임이 없습니다",
        newMeetingSoon: "곧 새로운 모임이 열릴 예정입니다!",
        
        // 결제 모달
        paymentTitle: "결제 안내",
        paymentMessage: "결제를 하셔야 신청이 확정됩니다.",
        bankInfo: "카카오뱅크(Kakao Bank) 3333-24-5091670 김*현",
        iPaid: "결제했습니다",
        processing: "처리 중...",
        
        // 확인 모달
        confirmationTitle: "신청 접수 완료",
        confirmationMessage: "신청이 접수되었습니다.\n1~2일 내에 확인 후 확정 여부를 안내해 드리겠습니다.",
        
        // 에러 메시지
        errorRegistering: "신청 중 문제가 발생했습니다.",
        errorServer: "서버와 통신 중 오류가 발생했습니다.",
        
        // 회원가입
        welcomeTitle: "Seoul Chess Club에 오신 것을 환영합니다",
        welcomeDesc: "SCC는 새로운 사람들을 만나고,\n도시를 탐험하며,\n관계를 깊게 만들어갑니다.",
        enterPhone: "시작하려면 전화번호를 입력하세요.",
        continue: "계속하기",
        smsConsent: "계속하면 SMS 수신에 동의하게 됩니다\n(언제든지 STOP을 보내 취소 가능)",
        
        // 회원 정보 입력
        tellAboutYourself: "자신에 대해 알려주세요",
        shareDetails: "커뮤니티에 참여하기 위해 정보를 공유해주세요",
        name: "이름",
        namePlaceholder: "홍길동",
        email: "이메일",
        emailPlaceholder: "your@email.com",
        gender: "성별",
        male: "남성",
        female: "여성",
        other: "기타",
        birthYear: "출생년도 (선택)",
        birthYearPlaceholder: "1990",
        chessExperience: "체스 경험",
        selectOption: "선택해주세요",
        noButWantLearn: "체스를 모르지만 배우고 싶어요",
        knowRulesOnly: "룰만 알아요",
        occasionallyPlay: "가끔 두는 편이에요",
        playWell: "잘 두는 편이에요",
        chessRating: "체스 레이팅 (선택)",
        dontKnow: "모르겠어요",
        under1000: "1000 미만",
        between1000_1500: "1000-1500",
        between1500_2000: "1500-2000",
        over2000: "2000 이상",
        signUp: "가입하기",
        registeringText: "등록 중...",
        
        // 성공/오류 메시지
        registrationSuccess: "회원가입이 완료되었습니다! 모임 목록으로 이동합니다... 🎉",
        registrationError: "회원가입 중 오류가 발생했습니다.",
        phoneError: "올바른 전화번호를 입력해주세요.",
        serverError: "서버와 통신 중 오류가 발생했습니다. 다시 시도해주세요.",
        
        // 대시보드
        dashboardTitle: "Community Control AI",
        dashboardSubtitle: "운영자 대시보드",
        newMeeting: "새 모임 추가",
        meetingTitle: "모임 제목",
        meetingTitlePlaceholder: "예: 11월 체스 모임",
        dateTime: "날짜 및 시간",
        location: "장소",
        locationPlaceholder: "예: 강남역 스타벅스",
        capacityLabel: "정원",
        capacityPlaceholder: "예: 20",
        createMeeting: "모임 생성",
        creatingMeeting: "생성 중...",
        participantList: "참가자 명단",
        totalVisits: "총 방문 횟수",
        registrationDate: "등록일",
        noParticipants: "등록된 참가자가 없습니다.",
        aiCsParser: "AI CS 파서 테스트",
        inputText: "카톡/DM 텍스트 입력",
        textPlaceholder: "고객 문의 텍스트를 여기에 붙여넣으세요...",
        analyze: "분석하기",
        analyzing: "분석 중...",
        aiResults: "AI 분석 결과",
    },
    en: {
        // Common
        back: "Back",
        confirm: "Confirm",
        cancel: "Cancel",
        loading: "Processing...",
        error: "Error",
        success: "Success",
        
        // Meeting List
        upcomingMeetings: "Upcoming Meetings",
        subtitle: "join us for chess, coffee, and great conversations",
        welcomeUser: ", which meeting would you like to join today?",
        registerPrompt: "Register and join the meeting!",
        registerButton: "Register",
        capacity: "Capacity",
        people: "people",
        registerMeeting: "Register",
        noMeetings: "No upcoming meetings",
        newMeetingSoon: "A new meeting will be held soon!",
        
        // Payment Modal
        paymentTitle: "Payment Instruction",
        paymentMessage: "The list is confirmed after the payment.",
        bankInfo: "Kakao Bank 3333-24-5091670 Kim*Hyun",
        iPaid: "I paid",
        processing: "Processing...",
        
        // Confirmation Modal
        confirmationTitle: "Application Received",
        confirmationMessage: "The application has been received.\nWe will confirm the application within 1-2 days.",
        
        // Error Messages
        errorRegistering: "An error occurred while registering.",
        errorServer: "An error occurred while communicating with the server.",
        
        // Registration
        welcomeTitle: "Welcome to Seoul Chess Club",
        welcomeDesc: "SCC helps you meet new people,\ndiscover your city, & deepen\nyour relationships.",
        enterPhone: "Enter your phone number to get started.",
        continue: "CONTINUE",
        smsConsent: "By continuing, you consent to receive SMS\n(text STOP to cancel anytime)",
        
        // User Information Input
        tellAboutYourself: "Tell us about yourself",
        shareDetails: "Share your details to join the community",
        name: "Name",
        namePlaceholder: "John Doe",
        email: "Email",
        emailPlaceholder: "your@email.com",
        gender: "Gender",
        male: "Male",
        female: "Female",
        other: "Other",
        birthYear: "Birth Year (Optional)",
        birthYearPlaceholder: "1990",
        chessExperience: "Chess Experience",
        selectOption: "Please select",
        noButWantLearn: "Don't know chess but want to learn",
        knowRulesOnly: "Know rules only",
        occasionallyPlay: "Occasionally play",
        playWell: "Play well",
        chessRating: "Chess Rating (Optional)",
        dontKnow: "I don't know",
        under1000: "Under 1000",
        between1000_1500: "1000-1500",
        between1500_2000: "1500-2000",
        over2000: "Over 2000",
        signUp: "SIGN UP",
        registeringText: "Registering...",
        
        // Success/Error Messages
        registrationSuccess: "Registration successful! Redirecting to the meeting list... 🎉",
        registrationError: "An error occurred during registration.",
        phoneError: "Please enter a valid phone number.",
        serverError: "An error occurred while communicating with the server. Please try again.",
        
        // Dashboard
        dashboardTitle: "Community Control AI",
        dashboardSubtitle: "Admin Dashboard",
        newMeeting: "Add New Meeting",
        meetingTitle: "Meeting Title",
        meetingTitlePlaceholder: "e.g., November Chess Meeting",
        dateTime: "Date & Time",
        location: "Location",
        locationPlaceholder: "e.g., Gangnam Station Starbucks",
        capacityLabel: "Capacity",
        capacityPlaceholder: "e.g., 20",
        createMeeting: "Create Meeting",
        creatingMeeting: "Creating...",
        participantList: "Participant List",
        totalVisits: "Total Visits",
        registrationDate: "Registration Date",
        noParticipants: "No registered participants.",
        aiCsParser: "AI CS Parser Test",
        inputText: "Input KakaoTalk/DM Text",
        textPlaceholder: "Paste customer inquiry text here...",
        analyze: "Analyze",
        analyzing: "Analyzing...",
        aiResults: "AI Analysis Results",
    }
};

// 현재 언어 감지
function detectLanguage() {
    // localStorage에 저장된 언어 설정 확인
    const savedLang = localStorage.getItem('preferred_language');
    if (savedLang) {
        return savedLang;
    }
    
    // 브라우저 언어 감지
    const browserLang = navigator.language || navigator.userLanguage;
    
    // 한국어면 'ko', 그 외는 'en'
    if (browserLang.startsWith('ko')) {
        return 'ko';
    }
    return 'en';
}

// 현재 언어
let currentLang = detectLanguage();

// 번역 함수
function t(key) {
    return translations[currentLang][key] || translations['en'][key] || key;
}

// 언어 변경 함수
function setLanguage(lang) {
    if (translations[lang]) {
        currentLang = lang;
        localStorage.setItem('preferred_language', lang);
        location.reload(); // 페이지 새로고침
    }
}

// 언어 토글 함수
function toggleLanguage() {
    const newLang = currentLang === 'ko' ? 'en' : 'ko';
    setLanguage(newLang);
}

// 전역으로 내보내기
window.t = t;
window.currentLang = currentLang;
window.setLanguage = setLanguage;
window.toggleLanguage = toggleLanguage;


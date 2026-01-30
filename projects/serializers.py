"""
Serializers for Projects app
"""
from rest_framework import serializers
from .models import Project, ProjectType, ProjectImage, ProjectFile
from customers.serializers import CustomerSerializer


class ProjectTypeSerializer(serializers.ModelSerializer):
    """Serializer for ProjectType"""
    
    class Meta:
        model = ProjectType
        fields = ['id', 'name', 'description', 'created_at']


class ProjectImageSerializer(serializers.ModelSerializer):
    """Serializer for ProjectImage"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectImage
        fields = ['id', 'project', 'image', 'image_url', 'caption', 'is_primary', 'uploaded_at']
        read_only_fields = ['uploaded_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ProjectFileSerializer(serializers.ModelSerializer):
    """Serializer for ProjectFile"""
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectFile
        fields = ['id', 'project', 'file', 'file_url', 'name', 'description', 'uploaded_at']
        read_only_fields = ['uploaded_at']
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project"""
    project_type_name = serializers.CharField(source='project_type.name', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    customer_email = serializers.CharField(source='customer.email', read_only=True)
    customer_whatsapp = serializers.CharField(source='customer.whatsapp_number', read_only=True)
    total_paid = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)
    files = ProjectFileSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'project_type', 'project_type_name',
            'customer', 'customer_name', 'customer_email', 'customer_whatsapp',
            'status', 'total_budget', 'total_revenue', 'total_cost',
            'profit', 'loss', 'total_paid', 'live_url', 'repository_url',
            'start_date', 'end_date', 'deadline', 'notes', 'images', 'files',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['profit', 'loss', 'created_at', 'updated_at']


class ProjectListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for project lists"""
    project_type_name = serializers.CharField(source='project_type.name', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    total_paid = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'project_type_name', 'customer_name', 'status',
            'total_budget', 'total_revenue', 'total_cost', 'profit', 'loss',
            'total_paid', 'live_url', 'primary_image', 'created_at'
        ]
    
    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary_image.image.url)
            return primary_image.image.url
        # Return first image if no primary
        first_image = obj.images.first()
        if first_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(first_image.image.url)
            return first_image.image.url
        return None

